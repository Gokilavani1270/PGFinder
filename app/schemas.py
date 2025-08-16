from pydantic import BaseModel

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
