import os

from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient

from radar_patient_check.main import app

load_dotenv(find_dotenv())

client = TestClient(app)

fake_key = os.getenv("FAKEKEY")
fake_identifier = os.getenv("FAKEIDENTIFIER")


def test_main():
    responce = client.get(
        f"/radar_check/{fake_identifier}",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 200
    assert responce.json() == True


def test_main_no_patient():
    responce = client.get(
        "/radar_check/6",
        headers={
            "Authorization": f"Bearer {fake_key}",
        },
    )
    assert responce.status_code == 200
    assert responce.json() == False


def test_main_no_token():
    response = client.get("/radar_check/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_main_not_found():
    responce = client.get("/radar_check/")
    assert responce.status_code == 404
    assert responce.json() == {"detail": "Not Found"}
