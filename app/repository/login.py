from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, db, token
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, ALGORITHM, SECRET_KEY
from datetime import timedelta
import jwt

def registerUser(user_data: schemas.CreateUser, db:Session = Depends(db.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already Registered")
    new_user = models.User(
        name = user_data.name,
        email = user_data.email,
        phno = user_data.phno,
        role = user_data.role
    )
    new_user.set_password(user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message" : "User {new_user.email} registered as {new_user.role} Successfully !"}

def loginUser(email: str, password: str, db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not user.check_password(password):   # 👈 FIXED
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.email, "role": user.role},   # 👈 include role for admin check
        expires_delta=access_token_expires
    )
   # print(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
    return {"message": "Logged In successfully!", "access_token": token, "token_type": "bearer"}
