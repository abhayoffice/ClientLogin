#signin.py
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from typing_extensions import Annotated
from db.client_db import authenticate_client
from db.hashing import Hash, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db
from schemas.client import ClientBase, ClientDisplay
from schemas.token import Token


router = APIRouter(
  prefix='/auth',
  tags=['auth']
)


@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session= Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # db = get_db()
    client = authenticate_client(form_data.username, form_data.password, db)
    if not client:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Hash.create_access_token(data={"sub": client.username}, expires_delta=access_token_expires)
    print("The access token is", access_token," and the token_type is bearer")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/client/me/"
    , response_model=ClientDisplay
    # , response_model=None
            )
async def read_users_me(current_client: Annotated[ClientDisplay, Depends(Hash.get_current_active_client)]):
    return current_client