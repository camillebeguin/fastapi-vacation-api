from datetime import timedelta

from sqlalchemy import Column, DateTime, Enum, ForeignKey, or_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_method

from app.core.enum import VacationType

from .base import BaseModel


class Vacation(BaseModel):
    __tablename__ = "vacation"
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employee.id"), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    type = Column(Enum(VacationType), nullable=False)

    @hybrid_method
    def is_contiguous(self, start_date, end_date):
        return or_(
            self.end_date == start_date - timedelta(days=1),
            self.start_date == end_date + timedelta(days=1),
        )