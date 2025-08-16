from fastapi import FastAPI
from .routers import login
from .db import Base, engine

app=FastAPI()

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
	return 'Hellow world'

app.include_router(login.router)
