import csv
import argparse
import os
import sys
import threading
import time
from prometheus_client import Counter, start_http_server

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.utils.postgres_writer import save_to_postgresql
from src.utils.elasticsearch_writer import save_to_elasticsearch
from src.utils.minio_uploader import save_to_s3
from src.utils.schema_validator import validate_data
from src.utils.logger import logger

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../../contracts/patient_vitals_v1.json")

# Prometheus metrics
ingested_rows = Counter('ingested_rows_total', 'Total number of successfully ingested rows')
failed_validations = Counter('failed_validations_total', 'Total number of failed row validations')
ingestion_errors = Counter('ingestion_errors_total', 'Total number of ingestion errors')


def start_metrics_server():
    """Start Prometheus metrics server on port 8000."""
    start_http_server(8000)


def read_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logger.info(f"Processing row: {row}")
            try:
                row['age'] = int(row['age'])
            except (ValueError, TypeError):
                logger.warning(f"Invalid age in row: {row}")
                failed_validations.inc()
                continue

            if validate_data(row, SCHEMA_PATH):
                try:
                    save_to_postgresql(row)
                    save_to_elasticsearch(row)
                    save_to_s3(data=row, bucket_name="unified-data-store")
                    ingested_rows.inc()
                except Exception as e:
                    ingestion_errors.inc()
                    logger.error(f"Error processing row {row}: {e}")
            else:
                failed_validations.inc()
                logger.warning(f"Validation failed for row: {row}")


if __name__ == "__main__":
    # Start Prometheus metrics server in background
    threading.Thread(target=start_metrics_server, daemon=True).start()

    parser = argparse.ArgumentParser(description='Batch Ingestor')
    parser.add_argument('--file', type=str, help='Path to the CSV file')
    args = parser.parse_args()
    read_csv(args.file)
    logger.info("Ingestion complete. Holding process to keep Prometheus metrics available...")
    while True:
        time.sleep(60)
