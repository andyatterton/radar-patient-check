import pytest
from fastapi.testclient import TestClient
from radar_patient_check.config import settings
from radar_patient_check.database import get_session
from radar_patient_check.main import app
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from ukrdc_sqla.ukrdc import Base as UKRDC3Base


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
            "nhsNumber": "9686368973",
            "dateOfBirth": "1968-02-12",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": True}


def test_main_radar_check_nhs_correct_dob_not(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "9658218881",
            "dateOfBirth": "1921-08-08",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": False}
