
#!/usr/bin/env python3
"""
Custom class-based context manager for database connections
"""

import sqlite3
import os

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
        
        # Create sample table and data for demonstration
        self._create_sample_data()
        
        return self.cursor
    
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
    
    def _create_sample_data(self):
        """Create sample users table with data"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT
            )
        ''')
        
        # Insert sample data
        sample_users = [
            ('Alice Johnson', 28, 'alice@email.com'),
            ('Bob Smith', 32, 'bob@email.com'),
            ('Charlie Brown', 45, 'charlie@email.com'),
            ('Diana Prince', 22, 'diana@email.com'),
            ('Eve Wilson', 35, 'eve@email.com')
        ]
        
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany(
                "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                sample_users
            )

if __name__ == "__main__":
    # Demonstrate usage of the context manager
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        print("Users in database:")
        print("-" * 40)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}")
