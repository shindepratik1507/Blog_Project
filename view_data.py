import sqlite3

conn = sqlite3.connect('instance/blog_database.db')
cursor = conn.cursor()

# Fetch all users
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()
print('Users:')
for user in users:
    print(user)

# Fetch all blogs
cursor.execute('SELECT * FROM blogs')
blogs = cursor.fetchall()
print('\\nBlogs:')
for blog in blogs:
    print(blog)

conn.close()
