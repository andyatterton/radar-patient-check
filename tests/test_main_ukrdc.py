from fastapi.testclient import TestClient

def test_main_ukrdc_check(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000001"},
        json={
            "nhsNumber": "9999999999",
            "dateOfBirth": "2001-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": True}


def test_main_ukrdc_check_no_patient(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000001"},
        json={
            "nhsNumber": "6",
            "dateOfBirth": "1900-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": False, "dateOfBirth": False}


def test_main_ukrdc_check_nhs_correct_dob_not(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000001"},
        json={
            "nhsNumber": "9999999999",
            "dateOfBirth": "1900-01-01",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"nhsNumber": True, "dateOfBirth": False}


def test_main_ukrdc_check_nhs_correct_dob_missing(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000001"},
        json={
            "nhsNumber": "9999999999",
        },
    )
    assert response.status_code == 422


def test_main_ukrdc_check_no_token(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        json={
            "nhsNumber": "9999999999",
            "dateOfBirth": "2001-01-01",
        },
    )
    assert response.status_code == 403


def test_main_ukrdc_check_bad_token(client: TestClient):
    response = client.post(
        "/ukrdc_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000000"},
        json={
            "nhsNumber": "9999999999",
            "dateOfBirth": "2001-01-01",
        },
    )
    assert response.status_code == 401
