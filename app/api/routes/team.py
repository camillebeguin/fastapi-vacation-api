from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.team import TeamRepository
from app.schema import TeamBase

router = APIRouter()

@router.post("", response_model=TeamBase)
def create_team(session: Session = Depends(get_db), *, obj_in: TeamBase):
    return TeamRepository.create(session=session, obj_in=obj_in)

@router.delete("/{team_id}")
def delete_team(session: Session = Depends(get_db), *, team_id: UUID):
    team = TeamRepository.get(session, id=team_id)
    return TeamRepository.delete(session=session, obj_in=team)