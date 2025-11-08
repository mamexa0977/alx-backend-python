#!/usr/bin/env python3
"""
Concurrent asynchronous database queries using aiosqlite
"""

import asyncio
import aiosqlite

async def initialize_database():
    """Initialize the database with sample data"""
    async with aiosqlite.connect("users.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT
            )
        ''')
        
        # Insert sample data if table is empty
        await db.execute("SELECT COUNT(*) FROM users")
        count = await db.fetchone()
        
        if count[0] == 0:
            sample_users = [
                ('Alice Johnson', 28, 'alice@email.com'),
                ('Bob Smith', 32, 'bob@email.com'),
                ('Charlie Brown', 45, 'charlie@email.com'),
                ('Diana Prince', 22, 'diana@email.com'),
                ('Eve Wilson', 35, 'eve@email.com'),
                ('Frank Miller', 52, 'frank@email.com'),
                ('Grace Lee', 41, 'grace@email.com')
            ]
            
            await db.executemany(
                "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                sample_users
            )
        
        await db.commit()

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print(f"Fetched {len(results)} users")
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print(f"Fetched {len(results)} users older than 40")
            return results

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather"""
    # Initialize database first
    await initialize_database()
    
    print("Starting concurrent database queries...")
    
    # Execute both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
        return_exceptions=True
    )
    
    # Handle results
    all_users, older_users = results
    
    print("\n" + "="*50)
    print("CONCURRENT QUERY RESULTS")
    print("="*50)
    
    print("\nAll Users:")
    print("-" * 30)
    for user in all_users:
        print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
    
    print("\nUsers Older Than 40:")
    print("-" * 30)
    for user in older_users:
        print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")
    
    return all_users, older_users

if __name__ == "__main__":
    # Run the concurrent queries
    asyncio.run(fetch_concurrently())
