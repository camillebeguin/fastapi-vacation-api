from datetime import date, datetime, timedelta
from uuid import UUID

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import aliased

from app.model import Employee, Vacation
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
    def _as_paginated_query(self, query, page, per_page):
        return query.count(), query.limit(per_page).offset((page - 1) * per_page).all() 
    
    def search_employees(self, session, search_term: str = None, page: int = 1, per_page: int = 10):
        filters = []

        if search_term:
            filters = [
                or_(
                    self.model.first_name.like(f'%{search_term}%'),
                    self.model.last_name.like(f'%{search_term}%'),
                )
            ]

        query = session.query(self.model).filter(*filters)
        return self._as_paginated_query(query=query, page=page, per_page=per_page)
    
    def get_employees_in_vacation(self, session, team_id: UUID = None, at_date: date = None, page: int = 1, per_page: int = 10):
        at_date = at_date or date.today()
        
        filters = [
            Vacation.start_date <= at_date, 
            Vacation.end_date >= at_date,
        ]

        if team_id:
            filters.append(self.model.team_id == team_id)

        query = (
            session.query(self.model)
            .join(Vacation, Vacation.employee_id == self.model.id)
            .filter(*filters)
        )

        return self._as_paginated_query(query, page, per_page)
    
    def get_employees_shared_vacations(self, session, employee_1: Employee, employee_2: Employee):
        """
        Return the days they will both be on vacation
        """
        vacation_1 = aliased(Vacation)
        vacation_2 = aliased(Vacation)

        overlap_period = (
            session.query(
                func.greatest(vacation_1.start_date, vacation_2.start_date).label("start_date"),
                func.least(vacation_1.end_date, vacation_2.end_date).label("end_date")
            )
            .join(
                vacation_2, 
                and_(
                    vacation_1.start_date <= vacation_2.end_date,
                    vacation_1.end_date >= vacation_2.start_date
                )
            )
            .filter(
                vacation_1.employee_id == employee_1.id, 
                vacation_2.employee_id == employee_2.id 
            )
            .group_by(
                vacation_1.id,
                vacation_2.id,
            )
            .all()
        )

        if not overlap_period:
            return {}
        
        overlap_dates = []
        for start_date, end_date in overlap_period:
            overlap_dates.extend(
                [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            )

        return set(sorted(overlap_dates))


EmployeeRepository = _EmployeeRepository(model=Employee)
