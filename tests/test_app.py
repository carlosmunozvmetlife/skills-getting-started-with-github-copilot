from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_success():
    # Arrange
    email = "teststudent@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_fails():
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_success():
    # Arrange
    email = "daniel@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/remove",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_remove_participant_not_found_fails():
    # Arrange
    email = "ghost@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/remove",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for activity"


def test_activity_not_found_fails():
    # Arrange
    email = "teststudent@mergington.edu"
    activity_name = "Nonexistent Activity"
    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
