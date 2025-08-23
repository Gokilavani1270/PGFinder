from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, db, token
from ..repository import reviews
from typing import List


admin_required = token.admin_required

router = APIRouter(
    prefix = '/reviews',
    tags = ['Reviews']
)

@router.post('/', response_model=schemas.ReviewBase)
def create_review(review_data: schemas.ReviewCreate, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    return reviews.create_review(review_data, db, current_user)

@router.get("/all", response_model=List[schemas.ReviewResponse])
def show_reviews(db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    return reviews.show_reviews(db, current_user)