# database.py
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import logging

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://localhost\\SQLEXPRESS01/master?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_db():
    logging.info("Acquiring a database connection.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logging.info("Database connection released.")
