import os
import boto3
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv()

# RDS credentials from environment variables
rds_host = os.getenv("RDS_HOST")
rds_user = os.getenv("RDS_USER")
rds_password = os.getenv("RDS_PASSWORD")
rds_database = os.getenv("RDS_DATABASE")

# S3 configuration
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
s3_file_key = os.getenv("S3_FILE_KEY")

def export_rds_to_s3():
    try:
        # Connect to RDS
        connection = mysql.connector.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            database=rds_database
        )
        
        if connection.is_connected():
            print("Connected to RDS instance.")
            
            cursor = connection.cursor()
            query = "SELECT * FROM patients;"  # Fetch all rows from the patients table
            cursor.execute(query)
            
            # Write data to a CSV file locally
            local_file = "patients_export.csv"
            with open(local_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([col[0] for col in cursor.description])  # Write headers
                writer.writerows(cursor.fetchall())  # Write rows
            
            print(f"Data exported to {local_file}.")
            
            # Upload CSV to S3
            s3 = boto3.client("s3")
            s3.upload_file(local_file, s3_bucket_name, s3_file_key)
            print(f"File uploaded to S3 at s3://{s3_bucket_name}/{s3_file_key}.")
            
            # Clean up local file
            os.remove(local_file)
            print(f"Local file {local_file} deleted.")
            
    except Error as e:
        print(f"Error connecting to RDS: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("Connection to RDS closed.")

# Run the function
export_rds_to_s3()
