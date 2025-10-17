from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    """Initialize the database with required tables"""
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect('instance/blog_database.db')
    cursor = conn.cursor()


    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # Create blogs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    """)


    # Create comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (blog_id) REFERENCES blogs (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)


    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('instance/blog_database.db')
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Custom Jinja2 filters for date formatting
@app.template_filter('format_date')
def format_date(date_str):
    """Format date string to readable format"""
    try:
        if isinstance(date_str, str):
            # Handle SQLite datetime format
            dt = datetime.fromisoformat(date_str.replace('Z', ''))
        else:
            dt = date_str
        return dt.strftime('%B %d, %Y')
    except:
        return str(date_str)


@app.template_filter('format_date_short')
def format_date_short(date_str):
    """Format date string to short readable format"""
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', ''))
        else:
            dt = date_str
        return dt.strftime('%b %d, %Y')
    except:
        return str(date_str)


@app.template_filter('time_ago')
def time_ago(date_str):
    """Show time ago format"""
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', ''))
        else:
            dt = date_str


        now = datetime.now()
        diff = now - dt


        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"
    except:
        return str(date_str)


# Template context processor
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.route('/')
def index():
    """Homepage - Display all blogs"""
    conn = get_db_connection()
    blogs = conn.execute("""
        SELECT b.*, u.name as author_name 
        FROM blogs b 
        JOIN users u ON b.author_id = u.id 
        ORDER BY b.created_at DESC
    """).fetchall()
    conn.close()
    return render_template('index.html', blogs=blogs)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')


        # Validation
        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('signup.html')


        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')


        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('signup.html')


        # Check if user already exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()


        if existing_user:
            flash('Email already registered!', 'error')
            conn.close()
            return render_template('signup.html')


        # Create new user
        hashed_password = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                    (name, email, hashed_password))
        conn.commit()


        # Get user id if needed
        # user_id = cursor.lastrowid  # Uncomment if needed


        conn.close()


        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))


    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')


        if not email or not password:
            flash('Email and password are required!', 'error')
            return render_template('login.html')


        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()


        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'error')


    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('index'))


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write_blog():
    """Write new blog post"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()


        if not title or not content:
            flash('Title and content are required!', 'error')
            return render_template('write_blog.html')


        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = f'uploads/{filename}'


        # Save blog to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO blogs (title, content, image_path, author_id) 
            VALUES (?, ?, ?, ?)
        """, (title, content, image_path, session['user_id']))
        conn.commit()


        # Get the newly created blog ID
        blog_id = cursor.lastrowid
        conn.close()


        flash('Blog published successfully!', 'success')
        return redirect(url_for('view_blog', id=blog_id))


    return render_template('write_blog.html')


@app.route('/blog/<int:id>')
def view_blog(id):
    """View individual blog post"""
    conn = get_db_connection()
    blog = conn.execute("""
        SELECT b.*, u.name as author_name 
        FROM blogs b 
        JOIN users u ON b.author_id = u.id 
        WHERE b.id = ?
    """, (id,)).fetchone()


    if not blog:
        flash('Blog not found!', 'error')
        conn.close()
        return redirect(url_for('index'))


    # Get comments for this blog
    comments = conn.execute("""
        SELECT c.*, u.name as commenter_name 
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.blog_id = ? 
        ORDER BY c.created_at DESC
    """, (id,)).fetchall()


    conn.close()
    return render_template('view_blog.html', blog=blog, comments=comments)


@app.route('/my_blogs')
@login_required
def my_blogs():
    """Display user's own blogs"""
    conn = get_db_connection()
    blogs = conn.execute("""
        SELECT * FROM blogs 
        WHERE author_id = ? 
        ORDER BY created_at DESC
    """, (session['user_id'],)).fetchall()
    conn.close()
    return render_template('my_blogs.html', blogs=blogs)


@app.route('/edit_blog/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    """Edit existing blog post"""
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE id = ? AND author_id = ?', 
                       (id, session['user_id'])).fetchone()


    if not blog:
        flash('Blog not found or you do not have permission to edit it!', 'error')
        conn.close()
        return redirect(url_for('my_blogs'))


    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()


        if not title or not content:
            flash('Title and content are required!', 'error')
            conn.close()
            return render_template('edit_blog.html', blog=blog)


        # Handle image upload
        image_path = blog['image_path']  # Keep existing image by default
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = f'uploads/{filename}'


        # Update blog in database
        conn.execute("""
            UPDATE blogs 
            SET title = ?, content = ?, image_path = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ? AND author_id = ?
        """, (title, content, image_path, id, session['user_id']))
        conn.commit()
        conn.close()


        flash('Blog updated successfully!', 'success')
        return redirect(url_for('view_blog', id=id))


    conn.close()
    return render_template('edit_blog.html', blog=blog)


@app.route('/delete_blog/<int:id>')
@login_required
def delete_blog(id):
    """Delete blog post"""
    conn = get_db_connection()
    blog = conn.execute('SELECT * FROM blogs WHERE id = ? AND author_id = ?', 
                       (id, session['user_id'])).fetchone()


    if not blog:
        flash('Blog not found or you do not have permission to delete it!', 'error')
    else:
        conn.execute('DELETE FROM blogs WHERE id = ? AND author_id = ?', 
                    (id, session['user_id']))
        conn.commit()
        flash('Blog deleted successfully!', 'success')


    conn.close()
    return redirect(url_for('my_blogs'))


@app.route('/like_blog/<int:id>')
@login_required
def like_blog(id):
    """Like a blog post"""
    conn = get_db_connection()
    conn.execute('UPDATE blogs SET likes = likes + 1 WHERE id = ?', (id,))
    conn.commit()


    # Get updated like count
    blog = conn.execute('SELECT likes FROM blogs WHERE id = ?', (id,)).fetchone()
    conn.close()


    return jsonify({'likes': blog['likes'] if blog else 0})


@app.route('/search')
def search():
    """Search blogs by title or author"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))


    conn = get_db_connection()
    blogs = conn.execute("""
        SELECT b.*, u.name as author_name 
        FROM blogs b 
        JOIN users u ON b.author_id = u.id 
        WHERE b.title LIKE ? OR u.name LIKE ?
        ORDER BY b.created_at DESC
    """, (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()


    return render_template('search_results.html', blogs=blogs, query=query)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5000)
