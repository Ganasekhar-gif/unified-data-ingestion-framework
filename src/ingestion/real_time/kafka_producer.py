from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_data = [
    {"patient_id": "P001", "age": 30, "diagnosis": "Diabetes"},
    {"patient_id": "P002", "age": 45, "diagnosis": "Hypertension"},
    {"patient_id": "P003", "age": 29, "diagnosis": "Asthma"},
]

for record in sample_data:
    producer.send('health-data', record)
    print(f"Sent: {record}")
    time.sleep(1)  # small delay to simulate streaming

producer.flush()
producer.close()
