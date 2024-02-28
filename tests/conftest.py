import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from ukrdc_sqla.ukrdc import Base as UKRDC3Base
from ukrdc_sqla.ukrdc import Patient, PatientNumber, ProgramMembership

from radar_patient_check.config import settings
from radar_patient_check.database import get_session
from radar_patient_check.main import app


def _create_test_data(session: Session):
    # Test patient with RADAR membership
    session.add(
        Patient(
            pid=1,
            birth_time=datetime.datetime(2000, 1, 1),
        )
    )

    session.add(
        PatientNumber(
            id=1, pid=1, patientid="8888888888", numbertype="NI", organization="NHS"
        )
    )

    session.add(
        ProgramMembership(
            id=1,
            pid=1,
            program_name="RADAR.COHORT.INS",
            to_time=None,
        )
    )

    # Test patient without RADAR membership

    session.add(
        Patient(
            pid=2,
            birth_time=datetime.datetime(2001, 1, 1),
        )
    )

    session.add(
        PatientNumber(
            id=2, pid=2, patientid="9999999999", numbertype="NI", organization="NHS"
        )
    )
    session.commit()


@pytest.fixture(name="session")
def session_fixture():
    """
    Create an in-memory test database and return a session.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    UKRDC3Base.metadata.tables["patient"].create(bind=engine)
    UKRDC3Base.metadata.tables["patientnumber"].create(bind=engine)
    UKRDC3Base.metadata.tables["programmembership"].create(bind=engine)

    with Session(engine) as session:
        _create_test_data(session)
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a test client and override the FastAPI dependency.
    Depends on the session fixture.
    """
    settings.radar_apikeys = ["PYTESTKEY0000000000"]
    settings.ukrdc_apikeys = ["PYTESTKEY0000000001"]

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()