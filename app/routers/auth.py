from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app import crud, schemas
from app.core.auth import create_access_token,  ACCESS_TOKEN_EXPIRE
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.crud_user.get_user_by_email(db, email=email)
    if user:
        raise HTTPException(status_code=400, detail="Email alreadu\y registered")
    new_user = crud.crud_user.create_user(db, schemas.UserCreate(email=email, password=password))
    return {"msg": "User created", "user_id": new_user.id}


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.crud_user.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE),
    )
    return {"access_token": access_token, "token_type": "bearer"}
