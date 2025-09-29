from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.crud import crud_feeding


router = APIRouter(prefix="/feedings", tags=["feedings"])

@router.post("/", response_model=schemas.FeedingRead)
def create_feeding(
        feeding: schemas.FeedingCreate,
        user_id: int,
        db: Session  = Depends(get_db)
):
    return crud_feeding.create_feeding(db, feeding, user_id)

@router.get("/", response_model=list[schemas.FeedingRead])
def get_feedings(db: Session = Depends(get_db)):
    return crud_feeding.get_feedings(db)
