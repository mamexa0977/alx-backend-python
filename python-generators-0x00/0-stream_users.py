#!/usr/bin/python3
"""
Stream users from database using generator
"""
import mysql.connector
from mysql.connector import Error

def connect_to_prodev():
    """Connects to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',      # Change as per your MySQL setup
            password='',      # Change as per your MySQL setup
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def stream_users():
    """
    Generator that streams rows from user_data table one by one
    Uses yield to implement generator pattern
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        # Only one loop as required
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    # Test the generator
    for user in stream_users():
        print(user)