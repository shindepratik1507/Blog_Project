import sqlite3

def count_users():
    # Connect to the SQLite database file
    conn = sqlite3.connect('instance/blog_database.db')
    cursor = conn.cursor()

    # Execute SQL query to count users
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    return user_count

if __name__ == '__main__':
    total = count_users()
    print(f'Total registered users in database: {total}')
