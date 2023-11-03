#!/bin/bash

# Start the Kafka consumer in the background
python -m consumer.consumer &

# Start the FastAPI application
uvicorn src.app:app --host 0.0.0.0 --port 80