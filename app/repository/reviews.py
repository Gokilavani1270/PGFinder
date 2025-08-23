from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, db, models, token

admin_required = token.admin_required


def create_review(review_data: schemas.ReviewCreate, db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pg = None
    if review_data.pg_name:
        pg = db.query(models.PG).filter(models.PG.name == review_data.pg_name).first()
    if not pg:
        raise HTTPException(status_code=404, detail="PG not found")
    
    new_review = models.Review(
        user_id=user.id,
        pg_id=pg.id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"id" : new_review.id,
            "pg_name" : pg.name,
            "user_name" : user.name,
            "rating" : review_data.rating,
            "comment" : review_data.comment
            }

def show_reviews(db: Session = Depends(db.get_db), current_user: dict = Depends(token.get_current_user)):
    if current_user["role"] == "admin":
        # Admin sees all Reviews
        reviews = db.query(models.Review).all()
    else:
        # Regular user sees only their Reviews
        user = db.query(models.User).filter(models.User.email == current_user["email"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        reviews = db.query(models.Review).filter(models.Review.user_id == user.id).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No Reviews available")
        
    result = []
    for r in reviews:
        result.append({
            "id": r.id,
            "pg_name": r.pg.name,
            "user_name": r.user.name,
            "rating" : r.rating,
            "comment" : r.comment
        })
    return result                       
