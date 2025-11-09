#!/usr/bin/env python3
"""
Decorator for logging database queries
"""

import sqlite3
import functools

def log_queries(func):
    """Decorator that logs SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get('query', None)
        if not query and args:
            # Try to find query in positional arguments
            for arg in args:
                if isinstance(arg, str) and arg.upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE')):
                    query = arg
                    break
        
        print(f"Executing query: {query}")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

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
    
    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users")
