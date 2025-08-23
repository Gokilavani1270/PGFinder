from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, db, token
from ..repository import bookings
from typing import List


admin_required = token.admin_required

router = APIRouter(
    prefix = '/bookings',
    tags = ['Bookings']
)

@router.post('/', response_model=schemas.BookingResponse)
def create_booking(booking_data: schemas.BookingCreate, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    return bookings.create_booking(booking_data, db, current_user)

@router.put("/{booking_id}", response_model=schemas.BookingResponse)
def update_booking_status(booking_id: int, status: str, db: Session = Depends(db.get_db), current_user: dict = Depends(admin_required)):
    return bookings.update_booking_status(booking_id, status, db)

# @router.get('/{booking_id}', response_model=schemas.BookingStatus)
# def show_booking_status(booking_id: int, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
#     return bookings.show_booking_status(booking_id, db)

@router.get("/all", response_model=List[schemas.BookingResponse])
def show_bookings(db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    return bookings.show_bookings(db, current_user)