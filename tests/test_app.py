from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_participant_raises_for_unknown_email():
    # Arrange
    email = "nope@example.com"

    # Act
    response = client.delete(
        f"/activities/Chess%20Club/participants?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
