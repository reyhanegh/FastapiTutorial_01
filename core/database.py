from sqlalchemy import create_engine, Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker,declarative_base, relationship
from fastapi import Depends
from datetime import datetime

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
    created_at = Column(DateTime(), default=datetime.now())
    user_id = Column(Integer,ForeignKey("users.id"))

    def __repr__(self):
        return f"Expense(id={self.id},user_id={self.user_id}, description={self.description}, amount={self.amount})"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)

    expenses = relationship("Expense", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"




def get_db():
    db = SessionLocal() 
    try:
        yield db        
    finally:
        db.close()