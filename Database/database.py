from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL= 'postgresql://postgres:admin@localhost:5432/blog'
engine= create_engine(DATABASE_URL)

SessionLocal= sessionmaker(bind= engine, autocommit=False, autoflush=False)

Base= declarative_base()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()