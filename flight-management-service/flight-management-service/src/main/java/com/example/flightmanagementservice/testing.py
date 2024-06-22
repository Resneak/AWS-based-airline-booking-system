import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        connection = psycopg2.connect(
            database="flight-management-db",
            user="adminX",
            password="EliteGaming275",
            host="flight-management-db.crguaws8egqt.us-east-2.rds.amazonaws.com",
            port="5432"
        )
        print("Connection to PostgreSQL DB successful")
        connection.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_connection()
