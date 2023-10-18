from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from app.core.enum import VacationType


class VacationBase(BaseModel):
    employee_id: UUID | None = None
    start_date: datetime
    end_date: datetime
    type: VacationType

    @model_validator(mode="after")
    def check_vacation_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start date cannot be before end date")
        
        if self.start_date.date() < date.today():
            raise ValueError("start date cannot be in the past")
        
        return self

