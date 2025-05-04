#!/bin/bash
/app/wait-for-it.sh postgres:5432 --timeout=30 --strict -- \
/app/wait-for-it.sh elasticsearch:9200 --timeout=30 --strict -- \
python src/ingestion/batch/batch_ingestor.py --file /app/test/test_data.csv
