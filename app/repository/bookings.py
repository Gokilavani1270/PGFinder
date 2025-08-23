from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, db, models, token

admin_required = token.admin_required


def create_booking(booking_data: schemas.BookingCreate, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pg = None
    if booking_data.pg_name:
        pg = db.query(models.PG).filter(models.PG.name == booking_data.pg_name).first()
    if not pg:
        raise HTTPException(status_code=404, detail="PG not found")
    new_booking = models.Booking(
        user_id=user.id,
        pg_id=pg.id,
        status="pending"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return {"id" : new_booking.id,
            "pg_name" : pg.name,
            "user_email" : user.email,
            "status" : new_booking.status
            }

def update_booking_status(booking_id: int, status: str, db: Session = Depends(db.get_db), current_user: dict = Depends(admin_required)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = status
    db.commit()
    db.refresh(booking)
    return {
        "id" : booking.id,
        "pg_name" : booking.pg.name,
        "user_email" : booking.user.email,
        "status" : booking.status
    }

# def show_booking_status(booking_id: int, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
#     booking = db.query(models.Booking).filter(models.Booking.id==booking_id).first()
#     if not booking_id:
#         raise HTTPException(status_code=404, detail = f"Booking with the id {booking_id} is not available")
#     return {
#         "id" : booking.id,
#         "pg_name" : booking.pg.name,
#         "user_email" : booking.user.email,
#         "status" : booking.status
#     }

def show_bookings(db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    if current_user["role"] == "admin":
        # Admin sees all bookings
        bookings = db.query(models.Booking).all()
    else:
        # Regular user sees only their bookings
        user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        bookings = db.query(models.Booking).filter(models.Booking.user_id == user.id).all()

    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings available")
        
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "status": b.status,
            "pg_name": b.pg.name,
            "user_email": b.user.email
        })
    return result                       