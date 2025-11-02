#!/usr/bin/python3
"""
Batch processing of large datasets
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

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        # First loop: batch processing
        while True:
            batch = []
            # Second loop: collecting batch
            for _ in range(batch_size):
                row = cursor.fetchone()
                if row is None:
                    break
                batch.append(row)
            
            if not batch:
                break
                
            yield batch
            
    except Error as e:
        print(f"Error streaming users in batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over age 25
    Uses only 3 loops as required
    """
    # Third loop: processing batches
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)

if __name__ == "__main__":
    batch_processing(50)