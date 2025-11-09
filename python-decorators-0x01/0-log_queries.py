#!/usr/bin/env python3
"""
Decorator for logging database queries with timestamps
"""

import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """Decorator that logs SQL queries with timestamps before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get('query', None)
        if not query and args:
            # Try to find query in positional arguments
            for arg in args:
                if isinstance(arg, str) and arg.upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE')):
                    query = arg
                    break
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if query:
            print(f"[{timestamp}] Executing query: {query}")
        else:
            print(f"[{timestamp}] Executing function: {func.__name__}")
        
        # Record start time for performance logging
        start_time = datetime.now()
        
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            print(f"[{timestamp}] Query completed in {execution_time:.4f} seconds")
            
            return result
            
        except Exception as e:
            # Log error with timestamp
            error_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{error_timestamp}] Query failed with error: {e}")
            raise
    
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetch all users from the database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

@log_queries
def create_users_table():
    """Create users table"""
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
    conn.commit()
    conn.close()
    print("Users table created/verified")

@log_queries  
def insert_sample_users():
    """Insert sample users into the database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    sample_users = [
        ('Alice Johnson', 28, 'alice@email.com'),
        ('Bob Smith', 32, 'bob@email.com'),
        ('Charlie Brown', 45, 'charlie@email.com'),
        ('Diana Prince', 22, 'diana@email.com'),
        ('Eve Wilson', 35, 'eve@email.com')
    ]
    
    cursor.executemany(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        sample_users
    )
    conn.commit()
    conn.close()
    print(f"Inserted {len(sample_users)} sample users")

def setup_database():
    """Setup sample database for testing"""
    # These calls will also be logged due to the decorator
    create_users_table()
    
    # Check if we need to insert sample data
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        insert_sample_users()

if __name__ == "__main__":
    print("=== Database Query Logger Demo ===")
    setup_database()
    
    print("\n=== Testing Query Logging ===")
    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users")
    
    # Test with a filtered query
    print("\n=== Testing Filtered Query ===")
    adult_users = fetch_all_users(query="SELECT * FROM users WHERE age >= 18")
    print(f"Retrieved {len(adult_users)} adult users")
    
    # Test with a specific column selection
    print("\n=== Testing Specific Columns ===")
    user_emails = fetch_all_users(query="SELECT name, email FROM users WHERE age > 30")
    print(f"Retrieved {len(user_emails)} users with age > 30")
    
    print("\n=== Demo Complete ===")
