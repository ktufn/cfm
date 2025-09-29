from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from app.core.security import get_password_hash, verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: id):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: id):
    userine = get_user(db, user_id)
    if not userine:
        return None
    db.delete(userine)
    db.commit()

    return userine

def authenticate_user(db: Session, email: str, password: str):
    userine = get_user_by_email(db, email)
    if not userine:
        return None
    if not verify_password(password, userine.password_hash):
        return None
    return userine
