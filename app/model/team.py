from sqlalchemy import Column, String

from .base import BaseModel


class Team(BaseModel):
    __tablename__ = "team"
    name = Column(String)
    
    