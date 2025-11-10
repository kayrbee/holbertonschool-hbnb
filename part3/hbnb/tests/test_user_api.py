import requests
import pytest
import uuid
from app import create_app, db
from config import TestConfig

BASE_URL = "http://127.0.0.1:5000/api/v1/users/"

# POST - Create a User
# Preconditions
# - Admin user exists
# - Admin user has valid jwt token


@pytest.fixture
def test_client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        # db.drop_all()


def test_create_user_valid(test_client):
    """ Create a user """
    unique_email = f"john.doe_{uuid.uuid4().hex}@example.com"
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": unique_email,
        "password": "password"
    }
    response = test_client.post(f"{BASE_URL}", json=payload)
    print("DEBUG STATUS:", response.status_code)
    print("DEBUG RESPONSE:", response.text)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == unique_email

# POST - Create a User (Invalid Email Format)


# def test_create_user_invalid_email():
#     """ Create a user (invalid email format) """
#     payload = {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": "invalid_email"
#     }
#     response = requests.post(f"{BASE_URL}/", json=payload)
#     assert response.status_code == 400
#     data = response.json()
#     assert data["error"] == "Invalid Email. Try again"

# # POST - Create User (Missing Required Field)


# def test_create_user_missing_field():
#     """ Create a user (missing required field) """
#     unique_email = f"sarah_{uuid.uuid4().hex}@example.com"
#     payload = {
#         "last_name": "Sarah",
#         "email": "sarah@example.com"
#     }
#     response = requests.post(f"{BASE_URL}/", json=payload)
#     print("DEBUG STATUS:", response.status_code)
#     print("DEBUG RESPONSE:", response.text)
#     assert response.status_code == 400
#     data = response.json()
#     assert "errors" in data
#     assert "first_name" in data["errors"]  # expect this to be missing
#     assert "required" in data["errors"]["first_name"].lower()

# GET - Retrieve All Existing Users


# def test_retrieve_all_users(test_client):
#     """ Retrieve all users """
#     response = test_client.get(f"{BASE_URL}/")
#     assert response.status_code == 200
#     users = response.json()
#     assert isinstance(users, list)

# GET - Retrieve Existing User by ID


# def test_retrieve_specific_user():
#     """ Retrieve one specific user by ID """
#     # create first
#     payload = {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": f"john.doe_{uuid.uuid4().hex}@example.com"
#     }
#     create_response = requests.post(f"{BASE_URL}/", json=payload)
#     user_id = create_response.json()["id"]

#     # retrieve
#     response = requests.get(f"{BASE_URL}/{user_id}")
#     print("DEBUG STATUS:", response.status_code)
#     print("DEBUG RESPONSE:", response.text)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["first_name"] == payload["first_name"]
#     assert data["last_name"] == payload["last_name"]
#     assert data["email"] == payload["email"]

# # GET - Non-existent User


# def test_retrieve_non_existent_user():
#     """ Retrieve a non-existent user """
#     fake_id = "00000000-0000-0000-0000-000000000000"
#     response = requests.get(f"{BASE_URL}/{fake_id}")
#     assert response.status_code == 404
#     data = response.json()
#     assert data["error"] == "User not found"

# # PUT - Update a User


# def test_update_user():
#     """ Update user information """
#     # create user first
#     payload = {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": f"john.doe_{uuid.uuid4().hex}@example.com"
#     }
#     create_response = requests.post(f"{BASE_URL}/", json=payload)
#     user_id = create_response.json()["id"]

#     # update user
#     update_payload = {
#         "first_name": "Jack",
#         "last_name": "Doe",
#         "email": payload["email"]
#     }
#     update_response = requests.put(
#         f"{BASE_URL}/{user_id}", json=update_payload)
#     assert update_response.status_code == 200
#     updated = update_response.json()
#     assert updated["first_name"] == "Jack"
