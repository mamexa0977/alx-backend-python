#!/usr/bin/env python3
"""
Retry decorator for database operations
"""

import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            raise e
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator that retries database operations on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"Success on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            
            print(f"All {retries} attempts failed")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

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
    
    # Attempt to fetch users with automatic retry on failure
    try:
        users = fetch_users_with_retry()
        print(f"Successfully retrieved {len(users)} users")
        for user in users:
            print(user)
    except Exception as e:
        print(f"Failed to fetch users: {e}")
