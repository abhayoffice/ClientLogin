#client.py
from sqlalchemy.orm.session import Session
from schemas.client import ClientBase, ClientDisplay
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from db.database import get_db
from db import client_db

router = APIRouter(
  prefix='/client',
  tags=['client']
)

# @router.post(''
#   # , response_model=ClientDisplay
#              )
# async def create_client(request: ClientBase, db: Session = Depends(get_db)):
#   new_client = await run_in_threadpool(client_db.create_user, db, request)
#
#   return new_client
@router.post('', response_model=ClientDisplay)
def create_client(request: ClientBase, db: Session = Depends(get_db)):
  return client_db.create_user(db, request)

