import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv()

# RDS credentials from environment variables
host = os.getenv("RDS_HOST")
user = os.getenv("RDS_USER")
password = os.getenv("RDS_PASSWORD")

try:
    # Connect to MySQL RDS instance without specifying a database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    if connection.is_connected():
        print("Successfully connected to RDS instance")
        
        cursor = connection.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")
        print("Database 'my_database' created or already exists.")
        
        # Select the newly created database
        cursor.execute("USE my_database;")
        print("Now using 'my_database'.")

        # Create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE,
            medication VARCHAR(100),
            dosage VARCHAR(50),
            medication_interval VARCHAR(50)  -- Renaming the column to avoid reserved keywords
        );
        """
        cursor.execute(create_table_query)
        print("Table 'patients' created or already exists.")

except Error as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")
