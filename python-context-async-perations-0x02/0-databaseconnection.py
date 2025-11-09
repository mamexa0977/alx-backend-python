#!/usr/bin/env python3
"""
Custom class-based context manager for database connections
"""

import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connections"""
    
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
    def __enter__(self):
        """Setup connection when entering context"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting context"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is not None:  # Exception occurred
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
        # Return False to propagate exceptions, True to suppress them
        return False
    
    def execute_query(self, query, params=None):
        """Execute a SQL query and return results"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

def create_sample_database():
    """Create sample database with users table and data"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert sample data only if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
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
        print("Sample data inserted into users table")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create the sample database first
    create_sample_database()
    
    # Use the context manager with the with statement
    # Perform the query SELECT * FROM users and print results
    print("Using DatabaseConnection context manager:")
    print("=" * 50)
    
    with DatabaseConnection() as db:
        results = db.execute_query("SELECT * FROM users")
        
        print("Users in database:")
        print("-" * 40)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}")
    
    print("\nContext manager successfully closed the database connection.")
