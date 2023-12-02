from fastapi import HTTPException, status
from db.models import DbClient
from schemas.client import ClientBase
from sqlalchemy.orm.session import Session
# from db.hashing import Hash

def create_user(db: Session, request: ClientBase, new_client=None):
  new_client = DbClient(
    username = request.username,
    email = request.email,
    # password = Hash.bcrypt(request.password)
    password = request.password
  )
  db.add(new_client)
  db.commit()
  db.refresh(new_client)
  return new_client

def get_user_by_username(db: Session, username: str):
  client = db.query(DbClient).filter(DbClient.username == username).first()
  if not client:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return client