# Unified Data Ingestion Layer

GitHub Repository: [https://github.com/Ganasekhar-gif/unified-data-ingestion-framework.git](https://github.com/Ganasekhar-gif/unified-data-ingestion-framework.git)                                                  
Architecture diagram: [https://github.com/user-attachments/assets/86920eb4-7490-42c2-b73e-ab960d03410f](https://github.com/user-attachments/assets/86920eb4-7490-42c2-b73e-ab960d03410f)                 

for details of architecture workflow please refer to: [architecture.md](architecture.md)

## Overview

This project is a centralized data ingestion system designed to handle both batch and streaming data efficiently. It reduces system complexity, removes hardcoded integrations, and centralizes data flow through Kafka as a message broker. The data pipeline routes data to multiple downstream systems such as PostgreSQL, Elasticsearch, and MinIO for storage, analysis, and monitoring. The system is designed with fault tolerance, retry mechanisms, and monitoring capabilities to ensure reliability.

## Key Features:

* Plug-and-play architecture for easy integration of new sources and sinks
* Support for both batch and real-time data sources
* Scalable ingestion layer with Kafka as the central message queue
* Downstream routing to PostgreSQL, Elasticsearch, and MinIO
* Metrics collection and monitoring via Prometheus and Grafana
* Centralized configuration using `.env` file for credentials and system parameters

## Expected Outcome:

* Centralized, scalable ingestion system improving reliability and onboarding speed
* Near real-time or scheduled data availability for downstream dashboards, alerts, and models
* Reduced manual effort in maintaining integrations and supporting new data sources

## Setup Instructions

### Prerequisites:

* Docker and Docker Compose installed on your system
* Python 3.x and pip (for local development and testing)
* MinIO, PostgreSQL, Elasticsearch, Prometheus, Grafana running in Docker containers

### Steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Ganasekhar-gif/unified-data-ingestion-framework.git
   cd unified-data-ingestion-framework
   ```

2. **Create a .env file**:
   Use the `.env.example` file as a template to create your own `.env` file containing required credentials and parameters. Modify the values as necessary for MinIO, PostgreSQL, etc.

3. **Build and Start Services**:
   Use Docker Compose to bring up the entire system:

   ```bash
   docker-compose up --build -d
   ```

4. **Access Services**:

* **Grafana**: [http://localhost:3001](http://localhost:3001)
* **Prometheus**: [http://localhost:9090](http://localhost:9090)
* **MinIO**: [http://localhost:9000](http://localhost:9000)
* **PostgreSQL**: Accessible via any SQL client with the credentials set in `.env`

5. **Running Batch Ingestor**:
   The batch ingestor service should be accessible at [http://localhost:8000](http://localhost:8000). It will process batch data and route it to downstream systems like PostgreSQL, Elasticsearch, and MinIO.

6. **Monitor Metrics**:
   Prometheus and Grafana will automatically collect and display metrics. The Prometheus service scrapes metrics from the batch ingestor.

### Troubleshooting

If you encounter issues with container start-up, try running:

```bash
docker-compose down
docker-compose up --build
```

## Usage Instructions

### Sending Data to the Ingestion Layer (Batch)

Data can be sent to the system through the batch ingestor service. The batch ingestor listens for HTTP POST requests and processes the data as it arrives.

#### Example:

**For Windows CMD:**

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"patient_id\": \"12345\", \"age\": 40, \"diagnosis\": \"Flu\"}" http://localhost:8000/ingest
```

**For Bash/Linux/macOS:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"patient_id": "12345", "age": 40, "diagnosis": "Flu"}' \
     http://localhost:8000/ingest
```

### Real-time Ingestion via Kafka

The system also supports real-time data ingestion using Kafka.

* **Kafka Producer**: Sends messages to the `ingestion-topic`
* **Kafka Consumer**: Listens to `ingestion-topic`, processes data, and stores it in downstream systems

#### Example (Kafka Console Producer):

```bash
Python src/ingestion/real_time/kafka_producer.py
```

### Example (kafka console consumer):
```bash
Python src/ingestion/real_time/kafka_consumer.py
```

Ensure Kafka and Zookeeper services are running.

### View Data in Dashboards

After ingestion (batch or real-time), data is routed to PostgreSQL, Elasticsearch, and MinIO.

* **Grafana**: [http://localhost:3001](http://localhost:3001)
* **Prometheus**: [http://localhost:9090](http://localhost:9090)

### Metrics Monitoring

Prometheus tracks metrics like:

* `ingested_rows_total`
* `failed_validations_total`
* `ingestion_errors_total`

These are visualized in Grafana dashboards.

## Architecture Diagram
Include a diagram to represent the system architecture. This should illustrate:

* Kafka as the central message broker
* Data sources (batch and real-time)
* Downstream storage systems (PostgreSQL, Elasticsearch, MinIO)
* Monitoring via Prometheus and Grafana
* Metrics flow and alerting setup (if applicable)

**(Use a tool like draw\.io, Lucidchart, or even a simple hand-drawn sketch to generate the diagram.)**

## Future Improvements

* **Retry Logic**: Implement custom retry mechanisms to handle ingestion failures.
* **Alert Manager**: Integrate Alertmanager with Prometheus for more advanced alerting capabilities.
* **Extended Integrations**: Add more data sources and sinks for scalability.
* **Security Enhancements**: Integrate proper authentication and authorization mechanisms.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Ganasekhar-gif/unified-data-ingestion-framework/blob/main/LICENSE) file for details.
