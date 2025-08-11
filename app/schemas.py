from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class Product(BaseModel):
    name: str
    price: Decimal
    description: str
    image_url: str
    task_id: str

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class Tasks(BaseModel):
    task_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    error: str | None = None

    class Config:
        from_attributes = True