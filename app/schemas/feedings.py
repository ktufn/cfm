from pydantic import BaseModel
from datetime import datetime

class FeedingBase(BaseModel):
    amount: float

class FeedingCreate(FeedingBase):
    pass

class FeedingRead(FeedingBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True