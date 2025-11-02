#!/usr/bin/python3
"""
Lazy loading paginated data using generators
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

def paginate_users(page_size, offset):
    """Fetch paginated users from database"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that implements lazy pagination
    Only one loop as required
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    # Test the pagination
    for page in lazy_pagination(100):
        for user in page:
            print(user)