from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from models import UserBaseModel


class TaskModel(BaseModel):
    summary: str = Field(min_length=2)
    description: Optional[str]
    status: str = Field(min_length=2)
    priority: str = Field(min_length=2)
    user_id: UUID


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: str
    priority: str
    user_id: UUID
    # user: UserBaseModel

    class Config:
        orm_mode = True
