from pydantic import BaseModel
from typing import Optional

# ---------------------- Schemas for Table User ----------------------

class CreateUser(BaseModel):
    name : str
    email : str 
    password : str
    phno : str
    role : str = "user"

class LoginUser(BaseModel):
    email : str 
    password : str

class MessageResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

# ---------------------- Schemas for Table PG ----------------------

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

class PGResponseUser(PGBase):
    pass

# ---------------------- Schema for Bookings ----------------------

class BookingBase(BaseModel):
    pg_name: str

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_email: str
    pg_name: str
    status: str

    class Config:
        orm_mode = True

class BookingStatus(BookingBase):
    status: str

    class Config:
        orm_mode = True


# ---------------------- Schema for Reviews ----------------------

class ReviewBase(BaseModel):
    pg_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True