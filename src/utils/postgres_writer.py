import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
from .logger import logger

load_dotenv()

def save_to_postgresql(data):
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()

        # Insert data into the health_data table
        cur.execute(
            """
            INSERT INTO health_data (patient_id, age, diagnosis, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (data['patient_id'], data['age'], data['diagnosis'], datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving to PostgreSQL: {e}")
