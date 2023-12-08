# client.py
from sqlalchemy.orm.session import Session
from schemas.client import ClientBase, ClientDisplay
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from db.database import get_db
from db import client_db
from logger import logging  # Assuming you have a logger instance already set up

router = APIRouter(
    prefix='/api/v1/auth/client',
    tags=['client']
)


@router.post('', response_model=ClientDisplay)
def create_client(request: ClientBase, db: Session = Depends(get_db)) ->ClientDisplay:
    logging.info("Received request to create a new client.")

    # Uncomment the following line to log the request details (optional)
    # logging.debug(f"Request details: {request}")

    try:
        new_client = client_db.create_user(db, request)
        logging.info("Client creation successful.")
        return new_client
    except Exception as e:
        logging.error(f"Error creating client: {e}")
        raise
