from enum import Enum
from datetime import datetime

from pydantic import BaseModel, EmailStr


class TransactionStatus(Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"
    FAILED = "Failed"


class ItemType(Enum):
    BOOK = "Book"
    MOVIE = "Movie"
    DVD_TV_SERIES = "DVD of TV Series"


class TransactionSchema(BaseModel):
    # Transaction details
    id_transaction: int
    transaction_time: datetime
    transaction_total_amount: float
    transaction_status: TransactionStatus
    # Item details
    item_id: str
    item_type: ItemType
    item_title: str
    item_description: str
    item_price: float
    # Client details
    client_id: int
    client_name: str
    client_email: EmailStr
    client_phone: str
    client_cpf: str
    # Employee details
    employee_id: int
    employee_name: str
    employee_role: str
    # Franchise details
    franchise_id: int
    franchise_name: str
    franchise_city: str
