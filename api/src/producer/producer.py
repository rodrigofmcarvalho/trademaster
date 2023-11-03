import json
import os

from kafka import KafkaProducer

from config.logger import logging

# Kafka configurations
KAFKA_BROKER = os.environ['KAFKA_BROKER']
SUCCESS_KAFKA_TOPIC = os.environ['SUCCESS_KAFKA_TOPIC']
FAILURE_KAFKA_TOPIC = os.environ['FAILURE_KAFKA_TOPIC']

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)


class Producer:
    @staticmethod
    def produce_event(event: dict, schema_validation: str) -> None:
        """
        Sends an event to the appropriate Kafka topic based on schema validation.

        The event is sent to SUCCESS_KAFKA_TOPIC if schema_validation is 'True',
        otherwise, it is sent to FAILURE_KAFKA_TOPIC. The method logs an info message on
        successful sending or an error message on failure.

        Args:
            event (dict): The event data to be sent.
            schema_validation (str): A string indicating whether the event passed schema validation.
                                    This should be the string 'True' if validation is successful, or
                                    any other value if not.

        Note:
            If an exception occurs while sending the event, the error is logged.
        """
        topic = (
            SUCCESS_KAFKA_TOPIC
            if schema_validation is True
            else FAILURE_KAFKA_TOPIC
        )
        try:
            producer.send(topic, event)
            logging.info(f'Sent event to {topic}')
        except Exception as e:
            logging.error(f'Failed to send the event to {topic}. Error: {e}')
