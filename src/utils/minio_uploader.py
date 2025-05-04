import boto3
import uuid
import os
from dotenv import load_dotenv
from .logger import logger

load_dotenv()

def save_to_s3(data, bucket_name):
    try:
        # Create an S3 client
        s3 = boto3.client(
            's3',
            endpoint_url='http://minio:9000',  
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
            region_name=os.getenv("MINIO_REGION")  
        )

        # Generate a unique filename using UUID
        file_name = f"{uuid.uuid4()}.json"

        # Upload the data to the specified bucket
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=str(data))
        
        # Log success
        logger.info(f"Successfully uploaded data to S3: {file_name}")
    except Exception as e:
        # Log any errors that occur during upload
        logger.error(f"Error saving to S3: {e}")
