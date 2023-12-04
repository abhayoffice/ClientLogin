# hashing.py
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import client_query
from schemas.client import ClientInHash
from schemas.token import TokenData

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "ae924eddd6d706c177c3e485c3b38e42eff4631f528b398ca69a37ad0e8fad91"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Hash():
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password : str, plain_password: str):
        print("-----------Hashed pw", hashed_password, " and plain pw", plain_password)
        return pwd_cxt.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict):
        expires_delta = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_client(db: Session = Depends(get_db()), token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials",
                                             headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credential_exception

            token_data = TokenData(username=username)
        except JWTError:
            raise credential_exception

        client = client_query.get_client_by_username(db, username=token_data.username)
        if client is None:
            raise credential_exception

        return client

    async def get_current_active_client(current_client: ClientInHash = Depends(get_current_client)):
        if current_client.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_client


