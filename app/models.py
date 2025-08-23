from sqlalchemy import Column, Integer, String, Float
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