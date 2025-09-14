from sqlalchemy import create_engine, Boolean, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker,declarative_base
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False # only for sqlite
}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50))
    amount = Column(Float())


def get_db():
    db = SessionLocal() 
    try:
        yield db        
    finally:
        db.close()