from uuid import UUID

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    first_name: str 
    last_name: str 
    team_id: UUID