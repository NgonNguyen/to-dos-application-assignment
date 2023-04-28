from sqlalchemy import Column, Uuid, Time, DateTime
import enum
import uuid


class Gender(enum.Enum):
    NONE = 'N'
    FEMALE = 'F'
    MALE = 'M'


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
