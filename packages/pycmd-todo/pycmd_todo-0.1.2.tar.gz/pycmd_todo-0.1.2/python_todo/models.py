"""Todo app models."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class PasswordChange(BaseModel):
    current_password: str
    new_password: str



class TodoStat(BaseModel):
    total: int = 0
    completed: int = 0
    pending: int = 0

class TodoUserBase(BaseModel):
    """Todo base model."""
    username: str


class TodoUserCreate(TodoUserBase):
    """Todo user create model."""
    password: str


class TodoUserRead(TodoUserBase):
    """Todo user read model."""
    id: int
    create_date: datetime


class TodoCreate(BaseModel):
    """Todo model."""
    user_id: int
    title: str
    done: bool = False



class TodoRead(BaseModel):
    """Todo read model."""
    id: int
    title: str
    done: bool = False
    create_date: datetime
