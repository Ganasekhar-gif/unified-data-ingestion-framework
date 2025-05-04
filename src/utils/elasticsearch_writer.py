from elasticsearch import Elasticsearch
from .logger import logger

es = Elasticsearch("http://elasticsearch:9200")

def save_to_elasticsearch(data):
    try:
        es.index(index="health_data", document=data)
    except Exception as e:
        logger.error(f"Elasticsearch Error: {e}")
