# signin.py
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import json
from sqlalchemy.orm.session import Session
from typing_extensions import Annotated

from db import client_db
from db.client_db import authenticate_client
from db.hashing import Hash, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db
from schemas.client import ClientBase, ClientDisplay
from schemas.token import Token
from logger import logging

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)


@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> json:
    logging.info("Received a request to generate an access token.")

    client = authenticate_client(form_data.username, form_data.password, db)

    if not client:
        logging.warning("Failed login attempt with incorrect username or password.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Hash.create_access_token(data={"sub": client.username}, expires_delta=access_token_expires)

    logging.info("Access token generated successfully.")
    logging.debug(f"Access token: {access_token}, Token type: bearer")

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/client/me/", response_model=ClientDisplay)
async def read_users_me(current_client: Annotated[ClientDisplay, Depends(client_db.get_current_active_client)]) ->ClientDisplay:
    logging.info("Received a request to get client details.")
    return current_client

# @router.post("/client/me/", response_model=ClientDisplay))
# async def read_users_me(current_client: Annotated[ClientDisplay, Depends(Hash.get_current_active_client)]) ->ClientDisplay:
#     logging.info("Received a request to get client details.")
#     return current_client
