from fastapi.testclient import TestClient

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
    assert response.status_code == 403


def test_main_radar_check_bad_token(client: TestClient):
    response = client.post(
        "/radar_check/",
        headers={"Authorization": "Bearer PYTESTKEY0000000001"},
        json={
            "nhsNumber": "8888888888",
            "dateOfBirth": "2000-01-01",
        },
    )
    assert response.status_code == 401
