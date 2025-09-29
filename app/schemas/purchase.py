from pydantic import BaseModel
from datetime import datetime

class PurchaseBase(BaseModel):
    amount: float

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseRead(PurchaseBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True

