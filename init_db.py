import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_database():
    """Create and initialize the database with sample data"""
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect('instance/blog_database.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create blogs table
    cursor.execute('''
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
    ''')

    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            blog_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (blog_id) REFERENCES blogs (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Insert sample users (password: password123 for all)
    sample_users = [
        ('Rajesh Kumar', 'rajesh@example.com', generate_password_hash('password123')),
        ('Priya Sharma', 'priya@example.com', generate_password_hash('password123')),
        ('Amit Patel', 'amit@example.com', generate_password_hash('password123')),
        ('Sneha Singh', 'sneha@example.com', generate_password_hash('password123'))
    ]

    for user in sample_users:
        cursor.execute('INSERT OR IGNORE INTO users (name, email, password) VALUES (?, ?, ?)', user)

    # Insert sample blogs
    sample_blogs = [
        ('Getting Started with Flask Web Development',
         'Flask is a lightweight WSGI web application framework written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. Flask offers suggestions, but does not enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. This flexibility makes Flask a great choice for both beginners and experienced developers who want full control over their components.',
         None, 1, 25),

        ('Mastering CSS Grid Layout',
         'CSS Grid Layout is a powerful layout system available in CSS. It is a 2-dimensional system, meaning it can handle both columns and rows, unlike flexbox which is largely a 1-dimensional system. You work with Grid Layout by applying CSS rules both to a parent element (which becomes the Grid Container) and to that element\'s children (which become Grid Items). In this comprehensive guide, we will explore all the features of CSS Grid.',
         None, 2, 42),

        ('JavaScript ES6+ Features You Should Know',
         'JavaScript has evolved significantly with ES6 and beyond. Features like arrow functions, destructuring, template literals, and async/await have transformed how we write JavaScript code. These modern features not only make code more readable and maintainable but also improve performance and developer experience. Let\'s explore the most important ES6+ features that every developer should master.',
         None, 3, 38),

        ('Building Responsive Web Applications',
         'In today\'s multi-device world, responsive web design is not optional—it\'s essential. Creating applications that work seamlessly across desktop, tablet, and mobile devices requires careful planning and implementation. This involves using flexible grid systems, responsive images, and media queries to create layouts that adapt to different screen sizes and orientations.',
         None, 1, 31),

        ('Database Design Best Practices',
         'Good database design is the foundation of any successful application. Whether you\'re working with SQL or NoSQL databases, following best practices ensures your application performs well, scales effectively, and maintains data integrity. This guide covers normalization, indexing strategies, relationship modeling, and performance optimization techniques.',
         None, 4, 29)
    ]

    for blog in sample_blogs:
        cursor.execute('''
            INSERT OR IGNORE INTO blogs (title, content, image_path, author_id, likes) 
            VALUES (?, ?, ?, ?, ?)
        ''', blog)

    conn.commit()
    conn.close()
    print("✅ Database created and populated with sample data!")
    print("\n📋 Sample Login Credentials:")
    print("Email: rajesh@example.com | Password: password123")
    print("Email: priya@example.com | Password: password123") 
    print("Email: amit@example.com | Password: password123")
    print("Email: sneha@example.com | Password: password123")

if __name__ == '__main__':
    create_database()
