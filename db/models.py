from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class DbClient(Base):
  __tablename__ = 'client'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)