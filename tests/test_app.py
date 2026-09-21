from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    assert response.status_code == 200
    assert email not in app.activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_participant_raises_for_unknown_email():
    response = client.delete(
        "/activities/Chess%20Club/participants?email=nope@example.com"
    )

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
