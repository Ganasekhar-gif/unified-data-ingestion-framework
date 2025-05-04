from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.utils.postgres_writer import save_to_postgresql
from src.utils.elasticsearch_writer import save_to_elasticsearch
from src.utils.minio_uploader import save_to_s3
from src.utils.schema_validator import validate_data
from src.utils.logger import logger

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../../contracts/patient_vitals_v1.json")

def consume_messages():
    if not os.path.exists(SCHEMA_PATH):
        logger.error(f"Schema file not found at: {SCHEMA_PATH}")
        sys.exit(1)

    try:
        consumer = KafkaConsumer(
            'health-data',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            group_id='medplat-group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
    except KafkaError as e:
        logger.error(f"Failed to start Kafka consumer: {e}")
        sys.exit(1)

    try:
        for message in consumer:
            data = message.value
            if validate_data(data, SCHEMA_PATH):
                try:
                    save_to_postgresql(data)
                    save_to_elasticsearch(data)
                    save_to_s3(data, 'unified-data-store')
                    logger.info(f"Processed message: {data}")
                except Exception as e:
                    logger.error(f"Error processing message {data}: {e}")
            else:
                logger.warning(f"Validation failed for message: {data}")
    except KeyboardInterrupt:
        logger.info("Kafka consumer interrupted by user. Shutting down.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
