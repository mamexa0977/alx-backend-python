#!/usr/bin/env python3
"""
Reusable query context manager
"""

import sqlite3

class ExecuteQuery:
    """Reusable context manager for executing database queries"""
    
    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params if params is not None else ()
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """Execute query when entering context"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup resources when exiting context"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is not None:  # Exception occurred
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()

if __name__ == "__main__":
    # Demonstrate usage with the specified query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery(query, params) as results:
        print("Users older than 25:")
        print("-" * 40)
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}")
