# client_db.py
from fastapi import HTTPException, status, Depends
from db.database import get_db
from db.models import DbClient
from schemas.client import ClientBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from schemas import client_query

def create_user(db: Session, request: ClientBase, new_client=None):
    hashed_password = Hash.bcrypt(request.password)
    new_client = DbClient(
        username=request.username,
        email=request.email,
        password=hashed_password  # Don't hash here; hashing will be done in hashing.py
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

def authenticate_client(username: str, password:str, db: Session):
    client = client_query.get_client_by_username(db, username)
    if not client:
        return False
    if not Hash.verify(password, client.password):
        return False
    return client

def create_password_reset_token(db: Session, email):
    return None