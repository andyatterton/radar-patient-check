import datetime

import pytest
from fastapi.testclient import TestClient
from radar_patient_check.config import settings
from radar_patient_check.database import get_session
from radar_patient_check.main import app
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from ukrdc_sqla.ukrdc import Base as UKRDC3Base
from ukrdc_sqla.ukrdc import Patient, PatientNumber, ProgramMembership


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
            program_name="RADAR",
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
    settings.apikeys = ["PYTESTKEY0000000000"]

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_main_radar_check(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "8888888888",
            "dateOfBirth": "2000-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": True}


def test_main_radar_check_no_patient(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "6",
            "dateOfBirth": "1900-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": False, "dateOfBirth": False}


def test_main_radar_check_nhs_correct_dob_not(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "8888888888",
            "dateOfBirth": "1900-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": False}


def test_main_radar_check_dob_correct_nhs_not(client: TestClient):
    # We need to make sure that any non-RADAR patients do not have their DoB "leaked" to the client.
    #   E.g. if a valid NHS number is given, but has no RADAR membership,
    #   the client should not be able to determine if the DoB was valid or not.

    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "9999999999",
            "dateOfBirth": "2001-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": False, "dateOfBirth": False}


def test_main_radar_check_nhs_correct_dob_missing(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "8888888888",
        },
    )
    assert response.status_code == 422


def test_main_radar_check_no_token(client: TestClient):
    response = client.post(
        "/radar_check/",
        json={
            "nhsNumber": "8888888888",
            "dateOfBirth": "2000-01-01",
        },
    )
    assert response.status_code == 401


def test_main_radar_check_bad_token(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer BADTOKEN"},
        json={
            "nhsNumber": "8888888888",
            "dateOfBirth": "2000-01-01",
        },
    )
    assert response.status_code == 401
