#!/usr/bin/python3
"""
Memory-efficient aggregation using generators
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

def stream_user_ages():
    """
    Generator that yields user ages one by one
    First loop: streaming ages from database
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield float(row[0])
            
    except Error as e:
        print(f"Error streaming ages: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates average age without loading entire dataset into memory
    Second loop: processing ages from generator
    """
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found")

if __name__ == "__main__":
    calculate_average_age()