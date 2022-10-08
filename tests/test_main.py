import os

from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient

from radar_patient_check.main import app

load_dotenv(find_dotenv())

client = TestClient(app)

fake_key = os.getenv("FAKEKEY")
fake_identifier = os.getenv("FAKEIDENTIFIER")
fake_date = os.getenv("FAKEDATE")


def test_main_radar_check():
    responce = client.get(
        f"/radar_check/?nhs_number={fake_identifier}&dob={fake_date}",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 200
    assert responce.json() == {"nhs_number": True, "dob": True}


def test_main_radar_check_no_patient():
    responce = client.get(
        "/radar_check/?nhs_number=6&dob=1900-01-01",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 200
    assert responce.json() == {"nhs_number": False, "dob": False}


def test_main_radar_check_nhs_correct_dob_not():
    responce = client.get(
        f"/radar_check/?nhs_number={fake_identifier}&dob=1900-01-01",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 200
    assert responce.json() == {"nhs_number": True, "dob": False}


def test_main_radar_check_nhs_correct_dob_missing():
    responce = client.get(
        f"/radar_check/?nhs_number={fake_identifier}",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 422
    assert responce.json() == {
        "detail": [
            {
                "loc": ["query", "dob"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_main_radar_check_no_token():
    response = client.get("/radar_check/?nhs_number=6&dob=1900-01-01")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_main_radar_check_no_parameters():
    responce = client.get(
        "/radar_check/",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 422
    assert responce.json() == {
        "detail": [
            {
                "loc": ["query", "nhs_number"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["query", "dob"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_main_radar_check_no_parameters_no_token():
    responce = client.get("/radar_check/")
    assert responce.status_code == 401
    assert responce.json() == {"detail": "Not authenticated"}
