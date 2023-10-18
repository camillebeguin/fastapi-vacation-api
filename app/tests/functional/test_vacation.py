from datetime import date

import freezegun
import pytest

from app import schema
from app.core.enum import VacationType
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository

freeze_date = date(2023, 1, 1)


def assert_vacation_dates(vacation, start_date, end_date):
    assert vacation.start_date.date() == start_date
    assert vacation.end_date.date() == end_date 

def assert_vacation_count(session, count: int):
    assert len(VacationRepository.get_many(session)) == count

def test_distinct_vacations(session, employee):
    with freezegun.freeze_time(freeze_date):
        vacation = VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )
        assert vacation.employee_id == employee.id 

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 9),
                end_date=date(2023, 1, 12),
                type=VacationType.paid,
            )
        )

        assert_vacation_dates(other_vacation, date(2023, 1, 9), date(2023, 1, 12))
        assert_vacation_count(session, 2)

def test_overlapping_vacations(session, employee):
    with freezegun.freeze_time(freeze_date):
        VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 5),
                end_date=date(2023, 1, 12),
                type=VacationType.paid,
            )
        )
        assert_vacation_dates(other_vacation, date(2023, 1, 1), date(2023, 1, 12))
        assert_vacation_count(session, 1)

def test_bounded_vacations(session, employee):
    with freezegun.freeze_time(freeze_date):
        VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 12),
                type=VacationType.paid,
            )
        )

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 5),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        assert_vacation_dates(other_vacation, date(2023, 1, 1), date(2023, 1, 12))
        assert_vacation_count(session, 1)

def test_unbounded_vacations(session, employee):
    with freezegun.freeze_time(freeze_date):
        VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 5),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 12),
                type=VacationType.paid,
            )
        )

        assert_vacation_dates(other_vacation, date(2023, 1, 1), date(2023, 1, 12))
        assert_vacation_count(session, 1)

def test_contiguous_vacations_same_type(session, employee):
    with freezegun.freeze_time(freeze_date):
        VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 8),
                end_date=date(2023, 1, 12),
                type=VacationType.paid,
            )
        )

        assert_vacation_dates(other_vacation, date(2023, 1, 1), date(2023, 1, 12))
        assert_vacation_count(session, 1)

def test_contiguous_vacations_different_type(session, employee):
    with freezegun.freeze_time(freeze_date):
        VacationRepository.create_vacation(
            session, 
            employee_id=employee.id,
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        other_vacation = VacationRepository.create_vacation(
            session,
            employee_id=employee.id, 
            vacation_in=schema.VacationBase(
                start_date=date(2023, 1, 8),
                end_date=date(2023, 1, 12),
                type=VacationType.unpaid,
            )
        )

        assert_vacation_dates(other_vacation, date(2023, 1, 8), date(2023, 1, 12))
        assert_vacation_count(session, 2)

def test_employee_shared_vacations(session, employee):
    with freezegun.freeze_time(freeze_date):
        # create another employee
        other_employee = EmployeeRepository.create(
            session, 
            obj_in=schema.EmployeeBase(
                first_name="Jane",
                last_name="Doe", 
                team_id=employee.team_id
            )
        )

        # create vacation for employee 1 and non overlapping vacation for employee 2
        VacationRepository.create(
            session, 
            obj_in=schema.VacationBase(
                employee_id=employee.id, 
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 7),
                type=VacationType.paid,
            )
        )

        VacationRepository.create(
            session, 
            obj_in=schema.VacationBase(
                employee_id=other_employee.id, 
                start_date=date(2023, 2, 1),
                end_date=date(2023, 2, 15),
                type=VacationType.paid,
            )
        )


        shared_vacation_days = EmployeeRepository.get_employees_shared_vacations(session, employee, other_employee)
        assert len(shared_vacation_days) == 0 

        # create overlapping vacation for employee 2
        VacationRepository.create(
            session, 
            obj_in=schema.VacationBase(
                employee_id=other_employee.id, 
                start_date=date(2023, 1, 6),
                end_date=date(2023, 1, 8),
                type=VacationType.paid,
            )
        )

        shared_vacation_days = EmployeeRepository.get_employees_shared_vacations(session, employee, other_employee)
        assert len(shared_vacation_days) == 2
        assert any(
            day.date() == date(2023, 1, 6) or day.date() == date(2023, 1, 7)
            for day in shared_vacation_days
        )