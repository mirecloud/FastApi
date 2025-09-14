from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  
from sqlmodel import  SQLModel, Session

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://admin:admin@192.168.52.1:5432/Fastapi"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"    

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for FastAPI
def get_session():
    with Session(engine) as session:
        yield session