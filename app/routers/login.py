from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, db
from ..repository import login
from .. import token

router = APIRouter(
    tags = ['User']
)

get_db = db.get_db

@router.post('/register', response_model=schemas.MessageResponse)
def registerUser(user_data: schemas.CreateUser, db:Session = Depends(db.get_db)):
    return login.registerUser(user_data, db)

@router.post('/login', response_model=schemas.LoginResponse)
def loginUser(email: str, password: str, db: Session = Depends(db.get_db)):
    return login.loginUser(email, password, db)

# @router.get("/secure-data")
# def get_secure_data(current_user: str = Depends(token.verify_access_token)):
#     return {"message": f"Hello {current_user}, you have access to secure data!"}