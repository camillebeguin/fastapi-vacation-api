from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class Employee(BaseModel):
    __tablename__ = "employee"
    first_name = Column(String)
    last_name = Column(String)
    team_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)

    team = relationship("Team", backref="employees", lazy="select")
    vacations = relationship("Vacation", backref="employee", uselist=True, lazy="select")