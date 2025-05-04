# Use an appropriate base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements_batch.txt .

# Install any dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements_batch.txt

# Copy the rest of the application code
COPY . .

# Copy wait-for-it script into the container
COPY wait-for-it.sh /app/

# Change file permissions to make the script executable (Linux-based)
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /app/wait-for-it.sh && chmod +x /app/wait-for-it.sh

# Set the entrypoint to wait for PostgreSQL and Elasticsearch before starting the Python script
ENTRYPOINT ["python", "src/ingestion/batch/batch_ingestor.py", "--file", "/app/test/test_data.csv"]
