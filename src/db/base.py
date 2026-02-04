from h11 import Data
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator
from config import DATABASE_URL

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine,
    
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        