#!/usr/bin/env python3
"""
Decorator for automatic database connection handling
"""

import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection as first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            raise e
        finally:
            conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone()

def setup_database():
    """Setup sample database for testing"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert sample data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ('Alice Johnson', 28, 'alice@email.com'),
            ('Bob Smith', 32, 'bob@email.com'),
            ('Charlie Brown', 45, 'charlie@email.com')
        ]
        cursor.executemany(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            sample_users
        )
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    setup_database()
    
    # Fetch user by ID with automatic connection handling 
    user = get_user_by_id(user_id=1)
    print(user)
