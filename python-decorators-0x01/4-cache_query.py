#!/usr/bin/env python3
"""
Cache decorator for database queries
"""

import time
import sqlite3 
import functools
import hashlib

query_cache = {}

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

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Create a cache key from the query
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[cache_key]
        
        # Execute query and cache result
        print(f"Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
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

def clear_cache():
    """Clear the query cache"""
    global query_cache
    query_cache.clear()
    print("Cache cleared")

if __name__ == "__main__":
    setup_database()
    
    # First call will cache the result
    print("=== First call ===")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users")
    
    # Second call will use the cached result
    print("\n=== Second call ===")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Retrieved {len(users_again)} users (from cache)")
    
    # Different query will execute and cache separately
    print("\n=== Different query ===")
    older_users = fetch_users_with_cache(query="SELECT * FROM users WHERE age > 30")
    print(f"Retrieved {len(older_users)} older users")
    
    # Test cache hit for the same query
    print("\n=== Same query again ===")
    older_users_again = fetch_users_with_cache(query="SELECT * FROM users WHERE age > 30")
    print(f"Retrieved {len(older_users_again)} older users (from cache)")
    
    # Show cache statistics
    print(f"\nCache contains {len(query_cache)} queries")
