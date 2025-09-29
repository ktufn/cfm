from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.crud import crud_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud_user.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email also registered")
    return crud_user.create_user(db, user)

@router.get("/", response_model=list[schemas.UserRead])
def get_users(db: Session = Depends(get_db)):
    all_u = crud_user.get_users(db)
    return all_u

@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found:(")
    return db_user

@router.delete("/{user_id}", response_model=schemas.UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.delete_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found:(")
    return db_user


