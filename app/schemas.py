from pydantic import BaseModel
from typing import Optional

# Schemas for Table User

class CreateUser(BaseModel):
    name : str
    email : str 
    password : str
    phno : str

class LoginUser(BaseModel):
    email : str 
    password : str

class MessageResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

# Schemas for Table PG

class PGBase(BaseModel):
    name: str
    address: str
    rooms: int
    rent: float
    amenities: Optional[str] = None

class PGCreate(PGBase):
    pass

class PGResponse(PGBase):
    id: int

    class Config:
        orm_mode = True

class PGUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    rooms: Optional[int]
    rent: Optional[float]
    amenities: Optional[str]

class PGUpdateResponse(BaseModel):
    message : str
    updated_pg : PGResponse