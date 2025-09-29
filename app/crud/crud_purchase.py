from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

def create_purchase(db: Session, purchase: schemas.PurchaseCreate, user_id: int):
    db_purchase = models.Purchase(
        amount=purchase.amount,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_purchases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Purchase).offset(skip).limit(limit).all()
