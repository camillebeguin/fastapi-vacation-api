from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema
from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[schema.EmployeeBase])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)

@router.post("", response_model=schema.EmployeeBase)
def create_employee(session: Session = Depends(get_db), *, obj_in: schema.EmployeeBase):
    return EmployeeRepository.create(session=session, obj_in=obj_in)

@router.post("/{employee_id}/vacation", response_model=Optional[schema.VacationBase])
def create_vacation(session: Session = Depends(get_db), *, employee_id: UUID, vacation_in: schema.VacationBase):
    return VacationRepository.create_vacation(session, employee_id, vacation_in)