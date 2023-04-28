import uuid
import enum
from database import Base
from sqlalchemy import Column, String, Uuid, Enum, SmallInteger
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity


class CompanyMode(enum.Enum):
    PRODUCT = 'P'
    OUTSOURCE = 'O'


class Company(Base):
    __tablename__ = "company"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False,
                  default=CompanyMode.PRODUCT)
    rating = Column(SmallInteger, nullable=False, default=0)
