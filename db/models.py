# db/models.py
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from logger import logging

class DbClient(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    reset_code = Column(String)

    logging.info("DbClient model defined.")

class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    strings = Column(String)
    timestamp = Column(DateTime)
    client_id = Column(Integer, ForeignKey('client.id'))
    # Uncomment and fill in the details for the relationship
    # client = relationship('DbClient', back_populates='posts')

    logging.info("DbPost model defined.")
