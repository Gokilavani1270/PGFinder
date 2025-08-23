from fastapi import FastAPI
from .routers import login, pg
from .db import Base, engine

app=FastAPI()

Base.metadata.create_all(bind = engine)

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
	return 'Hellow world'

app.include_router(login.router)
app.include_router(pg.router)