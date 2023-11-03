# consumer.py

import io
import json
import os
import boto3
import pandas as pd
from kafka import KafkaConsumer

class Consumer:
    def __init__(self):
        # Kafka Configurations
        self.kafka_broker = os.environ['KAFKA_BROKER']
        self.success_kafka_topic = os.environ['SUCCESS_KAFKA_TOPIC']

        # MinIO Configurations
        self.minio_endpoint = os.environ['MINIO_ENDPOINT']
        self.minio_access_key = os.environ['MINIO_ACCESS_KEY']
        self.minio_secret_key = os.environ['MINIO_SECRET_KEY']
        self.minio_bucket = os.environ['MINIO_BUCKET']

        # Kafka Consumer Initialization
        self.consumer = KafkaConsumer(
            self.success_kafka_topic,
            bootstrap_servers=self.kafka_broker,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
        )

        # MinIO Resource Initialization
        self.s3 = boto3.resource(
            's3',
            endpoint_url=self.minio_endpoint,
            aws_access_key_id=self.minio_access_key,
            aws_secret_access_key=self.minio_secret_key,
            config=boto3.session.Config(signature_version='s3v4'),
        )

    def consume_events(self) -> None:
        """
        This method continuously consumes messages from a Kafka topic. For each message,
        it extracts the event data and calls the method `save_to_parquet` to save the data
        as a Parquet file.
        """
        try:
            for message in self.consumer:
                event = message.value
                self.save_to_parquet(event)
        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            self.consumer.close()

    def save_to_parquet(self, event) -> None:
        """
        Converts the event data into a DataFrame and then saves it as a Parquet file in the
        specified directory structure within the MinIO bucket.

        Args:
            event (dict): The event data as a dictionary, which should include a 'transaction_time'
                          key among others, representing the time of the transaction.
        """
        transaction_time = pd.to_datetime(event['transaction_time'])
        event_date = transaction_time.date()
        df = pd.DataFrame([event])
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
        file_path = f'events/date={event_date}/sale_events.parquet'
        self.s3.Object(self.minio_bucket, file_path).put(Body=parquet_buffer.getvalue())

def main():
    consumer_instance = Consumer()
    consumer_instance.consume_events()

if __name__ == '__main__':
    main()