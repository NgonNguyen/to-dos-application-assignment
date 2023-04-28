from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from models import CompanyViewModel


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    company_id: UUID


class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    company_id: UUID

    class Config:
        orm_mode = True


class UserViewModel(UserBaseModel):
    is_admin: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    company_id: UUID
    # company: CompanyViewModel
