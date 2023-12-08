# hashing.py
from typing import Union, Any
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import timedelta, datetime

from logger import logging


pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
JWT_REFRESH_SECRET_KEY = "88e28b4f939861b6bddf2335bf30c337ce512a25d60361a9a6d88b69f3068d10"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

class Hash():
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        logging.debug("Verifying password.")
        return pwd_cxt.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    # def get_current_client(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Type[ClientInHash]:
    #     logging.debug("Getting current client.")
    #     credential_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )
    #
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         username: str = payload.get("sub")
    #
    #         if username is None:
    #             raise credential_exception
    #
    #         token_data = TokenData(username=username)
    #     except JWTError:
    #         raise credential_exception
    #
    #     client = client_db.get_client_by_username(db, username=token_data.username)
    #     my_client = ClientInHash
    #     my_client.email = client.email
    #     my_client.username = client.username
    #     if client is None:
    #         raise credential_exception
    #
    #     # return client
    #     return my_client


