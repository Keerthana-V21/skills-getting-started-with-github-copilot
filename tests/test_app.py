import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    # Use a unique email to avoid duplicate error
    response = client.post("/activities/Chess%20Club/signup?email=tester1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Clean up: remove the test participant
    data = client.get("/activities").json()
    if "tester1@mergington.edu" in data["Chess Club"]["participants"]:
        data["Chess Club"]["participants"].remove("tester1@mergington.edu")

def test_signup_duplicate():
    # Add a participant
    client.post("/activities/Chess%20Club/signup?email=tester2@mergington.edu")
    # Try to add again
    response = client.post("/activities/Chess%20Club/signup?email=tester2@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    data = client.get("/activities").json()
    if "tester2@mergington.edu" in data["Chess Club"]["participants"]:
        data["Chess Club"]["participants"].remove("tester2@mergington.edu")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
