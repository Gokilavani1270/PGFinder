from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phno = Column(String(10))
    role = Column(String, default="user")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete")
    reviews = relationship("Review", back_populates="user", cascade="all, delete")

    def set_password(self, password):
        self.password = pwd_cxt.hash(password)

    def check_password(self, password):
        return pwd_cxt.verify(password, self.password)
    
    
class PG(Base):
    __tablename__ = "pg"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    rooms = Column(Integer, nullable=False)
    rent = Column(Float, nullable=False)
    amenities = Column(String)
    bookings = relationship("Booking", back_populates="pg", cascade="all, delete")
    reviews = relationship("Review", back_populates="pg", cascade="all, delete")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pg_id = Column(Integer, ForeignKey("pg.id"))
    status = Column(String, default="pending")  # pending/approved/rejected

    user = relationship("User", back_populates="bookings")
    pg = relationship("PG", back_populates="bookings")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pg_id = Column(Integer, ForeignKey("pg.id"))
    rating = Column(Integer)  # 1–5
    comment = Column(String)

    user = relationship("User", back_populates="reviews")
    pg = relationship("PG", back_populates="reviews")