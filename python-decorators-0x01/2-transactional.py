#!/usr/bin/env python3
"""
Transaction management decorator
"""

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

def transactional(func):
    """Decorator that manages database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed successfully")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if cursor.rowcount == 0:
        raise ValueError(f"User with ID {user_id} not found")
    print(f"Updated email for user {user_id} to {new_email}")

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
    
    # Update user's email with automatic transaction handling 
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with invalid user ID to see rollback
    try:
        update_user_email(user_id=999, new_email='nonexistent@email.com')
    except Exception as e:
        print(f"Expected error: {e}")
