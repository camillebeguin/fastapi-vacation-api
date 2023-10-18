from app.repository.team import TeamRepository
from app.schema.team import TeamBase


def test_create_employee(session):
    team = TeamRepository.create(
        session=session, 
        obj_in=TeamBase(name="backend")
    )

    assert team.name == "backend"