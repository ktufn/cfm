from sqlalchemy.orm import Session

import app.schemas.feedings
from app import models, schemas
from datetime import datetime

def create_feeding(db: Session, feeding: schemas.FeedingCreate, user_id: int):
    db_feeding = models.Feeding(
        amount=feeding.amount,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_feeding)
    db.commit()
    db.refresh(db_feeding)
    return db_feeding

def get_feedings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Feeding).offset(skip).limit(limit).all()