from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from typing import Annotated
from fastapi import Depends
import os

# DATABASE_URL="postgresql://postgres:abinash@localhost:5432/transport"
DATABASE_URL = "postgresql://postgres:abinash@localhost:5432/transport"
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy=Annotated[Session,Depends(get_db)]