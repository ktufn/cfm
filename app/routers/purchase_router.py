from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import session_user

from app.database import get_db
from app import schemas
from app.crud import crud_purchase

router = APIRouter(prefix="/purchases", tags=["users"])

@router.post("/", response_model=schemas.PurchaseRead)
def create_purchase(purchase: schemas.PurchaseCreate, user_id: int,  db: Session = Depends(get_db)):
    return crud_purchase.create_purchase(db, purchase, user_id)

@router.get("/", response_model=list[schemas.PurchaseRead])
def get_purchases(db: Session = Depends(get_db)):
    return crud_purchase.get_purchases(db)
