import uuid
from database import Base
from sqlalchemy import Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity


class Task(Base, BaseEntity):
    __tablename__ = "task"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    summary = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)

    owner = relationship("User")
