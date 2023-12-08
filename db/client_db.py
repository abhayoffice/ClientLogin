# client_db.py
from datetime import timedelta
from typing import Type

from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.models import DbClient
from schemas.client import ClientBase, ClientResetPw, ClientDisplay, ClientInHash
from db.hashing import Hash, SECRET_KEY, ALGORITHM, oauth2_scheme
from logger import logging
from schemas.token import TokenData


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
    logging.info(f"User '{new_client.username}' created successfully.")
    return new_client

def authenticate_client(username: str, password: str, db: Session):
    client = get_client_by_username(db, username)
    if not client:
        logging.warning(f"Authentication failed for username '{username}': User not found.")
        return None
    if not Hash.verify(password, client.password):
        logging.warning(f"Authentication failed for username '{username}': Incorrect password.")
        return None
    logging.info(f"User '{username}' authenticated successfully.")
    return client

def get_client_by_email(db: Session, email: str) -> ClientResetPw:
    client = db.query(DbClient).filter(DbClient.email == email).first()
    my_client = ClientResetPw()
    my_client.id = client.id
    my_client.username = client.username
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with email {email} not found')
    # return client
    return my_client

def create_password_reset_token(db: Session, email: str):
    client = get_client_by_email(db, email)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )

    # Generate a password reset token with a short expiration time (e.g., 15 minutes)
    expires_delta = timedelta(minutes=15)
    token_data = {"sub": client.email}
    reset_token = Hash.create_access_token(token_data, expires_delta)
    return reset_token

def generate_reset_code(db: Session, email: str, new_pw: str):
    client = get_client_by_email(db, email)
    if not client:
        logging.warning(f"User with email {email} not found.")
        return None

    # Generate a reset code (you can use your own logic here)
    reset_code = "your_generated_reset_code"

    # Update the reset code and set the new password
    client.reset_code = reset_code
    client.password = Hash.bcrypt(new_pw)

    db.commit()
    db.refresh(client)

    logging.info(f"Reset code generated and password updated for user with email {email}.")
    return reset_code


def get_current_client(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> ClientInHash:
    logging.debug("Getting current client.")
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    client = get_client_for_validation(db, username=token_data.username)
    if client is None:
        raise credential_exception
    # my_client = ClientInHash
    # my_client.password = client

    # return client
    return client


def get_client_by_username(db: Session, username: str):
    my_client = ClientDisplay
    client = db.query(DbClient).filter(DbClient.username == username).first()
    my_client.email = client.email
    my_client.username = client.username
    # my_client = ClientDisplay.from_orm(client)
    print(">>>>>>>>>>>>>>>>>>>>Type of client",type(client))
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    # return client
    return my_client

def get_client_for_validation(db: Session, username: str):
    client = db.query(DbClient).filter(DbClient.username == username).first()
    # my_client = ClientDisplay.from_orm(client)
    print(">>>>>>>>>>>>>>>>>>>>Type of client",type(client))
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    # return client
    return ClientInHash(**client.password)

# def update_password_by_reset_code(db: Session, reset_code: str, new_pw: str) -> dict or None:
#     client = db.query(DbClient).filter(DbClient.reset_code == reset_code).first()
#     if not client:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with reset code {reset_code} not found",
#         )
#
#     # # Update the password and clear the reset code
#     # client.password = Hash.bcrypt(new_pw)
#     # client.reset_code = None
#     #
#     # db.commit()
#     # db.refresh(client)
#
#     return {"message": "Password updated successfully."}

def update_password_by_reset_code(db: Session, reset_code: str, new_pw: str) -> dict or None:
    client = db.query(DbClient).filter(DbClient.reset_code == reset_code).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with reset code {reset_code} not found",
        )

    # Update the password and clear the reset code
    client.password = Hash.bcrypt(new_pw)
    client.reset_code = None

    db.commit()
    db.refresh(client)

    return {"message": "Password updated successfully."}

def get_current_active_client(self, current_client:  Depends(get_current_client))->ClientInHash:
    logging.debug("Getting current active client.")
    if current_client.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_client
