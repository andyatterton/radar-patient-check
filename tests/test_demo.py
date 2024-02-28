from fastapi.testclient import TestClient

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
