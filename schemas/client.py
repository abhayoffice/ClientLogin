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