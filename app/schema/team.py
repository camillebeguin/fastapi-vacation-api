from uuid import UUID

from pydantic import BaseModel


class TeamBase(BaseModel):
    id: UUID | None = None 
    name: str 