import sys
from pathlib import Path

# Ensure the Flask project root folder is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from app import app


def extract_items(data, possible_keys):
    """
    Helper function to handle different JSON response structures.
    Some endpoints may return a list directly, while others may return
    a dictionary such as {"classes": [...]}.
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in possible_keys:
            if key in data and isinstance(data[key], list):
                return data[key]

    return []


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.is_json


def test_classes_endpoint(client):
    response = client.get("/classes")
    assert response.status_code == 200
    assert response.is_json


def test_trainers_endpoint(client):
    response = client.get("/trainers")
    assert response.status_code == 200
    assert response.is_json


def test_create_booking(client):
    classes_response = client.get("/classes")
    assert classes_response.status_code == 200

    classes_data = classes_response.get_json()
    classes = extract_items(classes_data, ["classes", "fitness_classes", "data"])

    if not classes:
        pytest.skip("No fitness classes available for booking test.")

    first_class = classes[0]
    class_id = (
        first_class.get("id")
        or first_class.get("class_id")
        or first_class.get("classId")
    )

    if not class_id:
        pytest.skip("No usable class ID found in class data.")

    payload = {
        "member_name": "Test User",
        "email": "test@example.com",
        "class_id": class_id,
        "notes": "Test booking request"
    }

    response = client.post("/bookings", json=payload)
    assert response.status_code in [200, 201]
    assert response.is_json


def test_create_enquiry(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Membership question",
        "message": "I would like to know more about membership plans."
    }

    response = client.post("/enquiries", json=payload)
    assert response.status_code in [200, 201]
    assert response.is_json
