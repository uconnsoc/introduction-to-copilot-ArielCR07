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
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=test1@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert "test1@mergington.edu" in result["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup?email=test2@mergington.edu")
    # Duplicate
    response = client.post("/activities/Programming Class/signup?email=test2@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid Activity/signup?email=test3@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_delete_success():
    # Signup first
    client.post("/activities/Gym Class/signup?email=test4@mergington.edu")
    # Then delete
    response = client.delete("/activities/Gym Class/signup?email=test4@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

def test_delete_not_signed_up():
    response = client.delete("/activities/Basketball Team/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]

def test_delete_invalid_activity():
    response = client.delete("/activities/Invalid Activity/signup?email=test5@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # TestClient follows redirects, so it should return the HTML content
    assert "<!DOCTYPE html>" in response.text
    assert "Mergington High School" in response.text