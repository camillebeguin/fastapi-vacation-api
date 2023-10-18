from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app import schema
from app.core.config import settings
from app.main import app
from app.repository.employee import EmployeeRepository
from app.repository.team import TeamRepository

APP_FOLDER = Path(__file__).parent.parent
DATABASE_URI = f"{settings.SQLALCHEMY_DATABASE_URI}_test"

@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(DATABASE_URI)

    if database_exists(DATABASE_URI):
        drop_database(DATABASE_URI)

    create_database(DATABASE_URI)
    return run_migrations(engine)

@pytest.fixture(scope="function")
def db_session_factory(db_engine):
    return sessionmaker(bind=db_engine)

def run_migrations(engine, rev="head"):
    alembic_config = APP_FOLDER / "alembic.ini"
    alembic_folder = APP_FOLDER / "alembic"
    cfg = Config(str(alembic_config))
    cfg.set_main_option("script_location", str(alembic_folder))
    cfg.set_main_option("sqlalchemy.url", DATABASE_URI)
    command.upgrade(cfg, "head")
    return engine

@pytest.fixture(scope="function")
def session(db_session_factory):
    session = db_session_factory()
    yield session  
    session.rollback() 
    session.close()

@pytest.fixture 
def api_client() -> TestClient:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def employee(session):
    team = TeamRepository.create(session, schema.TeamBase(name="backend"))
    return EmployeeRepository.create(
        session=session, 
        obj_in=schema.EmployeeBase(
            first_name="John",
            last_name="Doe", 
            team_id=team.id
        )
    )