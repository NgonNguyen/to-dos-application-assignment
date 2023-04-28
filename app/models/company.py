from typing import Optional
from pydantic import BaseModel, Field
from schemas import CompanyMode
from uuid import UUID


class CompanyModel(BaseModel):
    name: str = Field(min_length=2)
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.PRODUCT)
    rating: int = Field(ge=0, le=5, default=0)


class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    mode: CompanyMode = Field(default=CompanyMode.PRODUCT)
    rating: int = Field(ge=0, le=5, default=0)

    class Config:
        orm_mode = True
