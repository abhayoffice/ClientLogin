from pydantic import BaseModel
from datetime import datetime
from typing import List

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
    strings : str
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