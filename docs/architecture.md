# Architecture Overview

## 📌 Project Name:
**Unified Data Ingestion Layer**

---

## 📊 Architecture Diagram

Refer to the [Architecture Diagram Image](https://github.com/user-attachments/assets/86920eb4-7490-42c2-b73e-ab960d03410f) for a visual representation of the system layout and data flow.

---

## Architecture workflow:
graph TD
  subgraph Producers
    A1[Batch Ingestor (HTTP API)]
    A2[Real-Time Producer (Kafka Producer)]
  end

  subgraph Kafka Layer
    B[Kafka Topics]
  end

  subgraph Consumers
    C[Kafka Consumer Service]
  end

  subgraph Storage Systems
    D1[PostgreSQL]
    D2[Elasticsearch]
    D3[MinIO]
  end

  subgraph Monitoring
    E1[Prometheus]
    E2[Grafana]
  end

  A1 --> B
  A2 --> B
  B --> C
  C --> D1
  C --> D2
  C --> D3
  C --> E1
  E1 --> E2


## 🎯 Objective:
This system is designed to serve as a centralized and scalable data ingestion layer for handling **both batch and real-time data**. It facilitates seamless integration with multiple downstream storage and monitoring systems, making it easy to ingest, route, store, and monitor data with reliability and flexibility.

---

## 🏗️ System Architecture

### 🧩 Core Components:

#### 1. **Kafka (Message Broker)**
- Acts as the central communication hub between producers (data sources) and consumers (data processors).
- Supports real-time data flow via topics.

#### 2. **Data Producers**
- **Batch Ingestor:** Accepts HTTP POST requests with JSON data and sends it to Kafka.
- **Real-Time Producer:** Publishes streaming data (e.g., sensor data, logs) directly to Kafka topics.

#### 3. **Data Consumers**
- **Kafka Consumer Service:** Listens to Kafka topics, processes messages, validates them, and routes to downstream targets.

#### 4. **Downstream Systems**
- **PostgreSQL:** Stores structured, relational data.
- **Elasticsearch:** Stores logs and supports advanced text search and analytics.
- **MinIO:** Object storage for large datasets, files, and unstructured content.

#### 5. **Monitoring & Observability**
- **Prometheus:** Scrapes metrics from ingestion services and exposes them.
- **Grafana:** Visualizes metrics through dashboards.
- **Custom Metrics:** Tracks rows ingested, validation failures, and errors.

---

## 🧮 Data Flow

1. **Data Ingestion**
   - Batch or real-time data is sent via HTTP API or directly through Kafka producer.
2. **Kafka Routing**
   - Kafka acts as the event bus and distributes messages to consumers.
3. **Data Processing**
   - Kafka consumers validate and enrich data if needed.
4. **Storage & Archival**
   - Cleaned data is sent to PostgreSQL, Elasticsearch, or MinIO based on type and purpose.
5. **Monitoring**
   - Prometheus scrapes ingestion metrics.
   - Grafana displays ingestion health, volume, and failure rates.

---

## ⚙️ Tech Stack

| Component      | Technology         |
|----------------|--------------------|
| Message Queue  | Apache Kafka       |
| Batch API      | FastAPI (Python)   |
| Storage        | PostgreSQL, MinIO, Elasticsearch |
| Monitoring     | Prometheus, Grafana|
| Containerization | Docker, Docker Compose |
| Configuration  | .env file for secrets and system params |

---

## 📈 Metrics Monitored

- `ingested_rows_total`: Total number of successfully ingested rows.
- `failed_validations_total`: Count of records failing validation checks.
- `ingestion_errors_total`: Number of ingestion processing errors.



## 📌 Key Design Principles

- **Modularity:** Plug-and-play new data sources and sinks.
- **Fault Tolerance:** Kafka buffering and retry mechanisms.
- **Observability:** Built-in metrics, logging, and dashboards.
- **Scalability:** Easily extensible for more topics, producers, and consumers.

---
