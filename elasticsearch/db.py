"""Elasticsearch."""

from elasticsearch import Elasticsearch, NotFoundError
from os import environ

ELASTIC_USERNAME = environ["ELASTIC_USERNAME"]
ELASTIC_PASSWORD = environ["ELASTIC_PASSWORD"]
INDEX_NAME = "hades_missions"

client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

mappings = {
    "properties": {
        "timestamp": {
            "type": "date"
        },
        "sender": {
            "type": "keyword"
        },
        "receiver": {
            "type": "keyword"
        },
        "message": {
            "type": "text"
        },
        "tool_calls": {
            "type": "nested",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "keyword"
                },
                "arguments": {
                    "type": "object",
                    "enabled": True
                }
            }
        },
    }
}

try:
    response = client.indices.get(index=INDEX_NAME)
    print("Index already exists")
    print(response)
except NotFoundError as error:
    print("Creating the index")
    response = client.indices.create(index=INDEX_NAME, body={"mappings": mappings})
    print(response)

#print(client.indices.delete(index=INDEX_NAME))