#schemas/client.py
from pydantic import BaseModel
from datetime import datetime
from typing import List
from logger import logging

class ClientBase(BaseModel):
    username: str
    email: str
    password: str


class ClientDisplay(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode = True

class ClientPostBase(BaseModel):
    id: int
    strings: str
    pass

class Client(BaseModel):
    username: str

class ClientInHash(ClientBase):
    password: str

class ClientPostDisplay(BaseModel):
    id: int
    strings: str
    timestamp: datetime
    client: Client
    class Config():
        orm_mode = True


class ResetPassword(BaseModel):
    username: str
    new_pass: str
    reset_code: str

class ClientResetPw(BaseModel):
    # def __init__(self):
    #     self.email = None
    id: int
    username: str
    email: str
    # new_pass: str
    class Config():
        orm_mode = True
