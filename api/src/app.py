import json
import os
from datetime import datetime
from enum import Enum

import config.config as config
import config.logger as logger
from dotenv import load_dotenv
from fastapi import FastAPI
from producer.producer import Producer
from pydantic import ValidationError
from schema.schema import TransactionSchema

app = FastAPI()

logger = logger.setup_logger()

load_dotenv()
conf = getattr(config, f'{os.environ["APP_ENV"].title()}Config')


def custom_encoder(obj) -> str:
    """
    Custom JSON encoder function that handles the serialization of datetime and Enum types.

    Args:
        obj (object): The object to be encoded. This could be of type datetime or Enum.

    Raises:
        TypeError: If the object is not of type datetime or Enum, a TypeError will be raised,
                   indicating that the object is not JSON serializable.

    Returns:
        str: If the object is of type datetime, it returns the ISO format of the datetime.
        str: If the object is of type Enum, it returns the value of the Enum.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')


app = FastAPI(
    docs_url=f'/api/{conf.V_API}/docs',
    redoc_url=f'/api/{conf.V_API}/redoc',
    openapi_url=f'/api/{conf.V_API}/openapi.json',
)


@app.get(f'/api/{conf.V_API}')
async def root():
    return {'message': f'Welcome to the API {conf.V_API}!'}


@app.post(f'/api/{conf.V_API}{conf.SEND_SALE_PATH}')
async def send_sale_event(event: dict):
    try:
        validated_data = TransactionSchema.model_validate(event)
        json_data = validated_data.json()
        dict_data = json.loads(json_data)
        Producer.produce_event(dict_data, True)
        logger.info(f'Event matching the schema {event}')
        return 'Event emmitted successfully.'
    except ValidationError as e:
        logger.error(f'Schema mismatch for event: {event}. Error: {e}')
        error_event = {
            'original_event': event,
            'error_message': str(e),
            'error_details': e.errors() if hasattr(e, 'errors') else None,
        }
        Producer.produce_event(error_event, False)
        return {
            'message': f'Failed due to schema mismatch: {event}',
            'error': str(e),
        }
    except Exception as e:
        logger.error(f'Failed to process event: {event}. Error: {e}')
        return {
            'message': f'Failed to process event: {event}',
            'error': str(e),
        }
