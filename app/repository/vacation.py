from datetime import timedelta
from uuid import UUID

from sqlalchemy import or_

from app.model import Vacation
from app.repository.base import BaseRepository
from app.schema import VacationBase


class _VacationRepository(BaseRepository):
    def get_overlapping_vacations(self, session, vacation: Vacation):
        filters = [
            self.model.employee_id == vacation.employee_id, 
            self.model.end_date >= vacation.start_date - timedelta(days=1),
            self.model.start_date <= vacation.end_date + timedelta(days=1)
        ]
        
        return (
            session.query(self.model)
            .filter(*filters)
            .all()
        )
    
    def check_vacations_to_merge(self, session, vacation_in: VacationBase):
        if not (overlap_vacations := self.get_overlapping_vacations(session, vacation_in)):
            return 
        
        if any(
            v.type != vacation_in.type and v.is_contiguous(vacation_in.start_date, vacation_in.end_date) is False
            for v in overlap_vacations
        ):
            raise ValueError("cannot merge vacations of different types")
        
        return [v for v in overlap_vacations if v.type == vacation_in.type]
    
    def create_vacation(self, session, employee_id: UUID, vacation_in: VacationBase):
        vacation_in.employee_id = vacation_in.employee_id or employee_id
        
        if not (merge_vacations := self.check_vacations_to_merge(session, vacation_in)):
            return self.create(session, vacation_in)

        # merge vacations of same type into one
        updated_vacation = merge_vacations[0]
        updated_vacation.start_date = min([v.start_date for v in merge_vacations] + [vacation_in.start_date]) 
        updated_vacation.end_date = max([v.end_date for v in merge_vacations] + [vacation_in.end_date])

        for vacation in merge_vacations[1:]:
            self.delete(session, vacation)

        return self.save(session, updated_vacation)

VacationRepository = _VacationRepository(model=Vacation)