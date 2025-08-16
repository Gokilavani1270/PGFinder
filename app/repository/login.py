from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, db, token

def registerUser(user_data: schemas.CreateUser, db:Session = Depends(db.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already Registered")
    new_user = models.User(
        name = user_data.name,
        email = user_data.email,
        phno = user_data.phno
    )
    new_user.set_password(user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message" : "User registered Successfully !"}

def loginUser(user_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(db.get_db)):
    email = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not email or not email.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = token.create_access_token(data={"sub": email.email})
    return {"message" : "Logged In successfully !", "access_token":access_token, "token_type":"bearer"}