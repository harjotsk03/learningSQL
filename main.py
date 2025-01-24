import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv()

db_config = {
    "host": os.getenv("RDS_HOST"),
    "user": os.getenv("RDS_USER"),
    "password": os.getenv("RDS_PASSWORD"),
    "database": os.getenv("RDS_DATABASE")
}

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients;")
        patients = cursor.fetchall()
        return jsonify(patients)
    except mysql.connector.Error as err:
        return {"error": str(err)}, 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
