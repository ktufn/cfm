from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

# from app.models import Feeding

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    purchases = relationship("Purchase", back_populates="user", cascade="all, delete-orphan")
    feedings = relationship("Feeding", back_populates="user", cascade="all, delete-orphan")

