from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./pgfinder.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from .models import User, PG    #Add this line if we are creating more than one table in db and import all the tables name
    Base.metadata.create_all(bind = engine)
    print("Tables created!")

if __name__ == "__main__":
    create_tables()