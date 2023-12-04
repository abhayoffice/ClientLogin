# client_query.py
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from db.models import DbClient

def get_client_by_username(db: Session, username: str):
    client = db.query(DbClient).filter(DbClient.username == username).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return client
