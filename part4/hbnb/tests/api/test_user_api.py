import unittest
import uuid
from app import create_app, db
from config import TestConfig
import tests.api.helper_methods as setup

BASE_URL = "/api/v1/users/"


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """ Set up before each test """
        # Create a fresh app and db before each test
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.app.testing = True
        self.client = self.app.test_client()

        # Create an admin
        self.admin = setup.create_test_user(is_admin=True)
        self.admin_token = setup.login(self.admin)
        self.admin_auth_header = {
            "Authorization": f'Bearer {self.admin_token}'}

        # Create a payload
        self.unique_email = f"john.doe_{uuid.uuid4().hex}@example.com"
        self.user_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": self.unique_email,
            "password": "password"
        }

    # <-- Tests start here -->

    # <-- This section covers successful CRUD operations -->

    def test_create_user_valid(self):
        response = self.client.post(
            f"{BASE_URL}",
            headers=self.admin_auth_header,
            json=self.user_payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertIn(data["message"], "User registered successfully")

    def test_delete_user(self):
        # Create a user
        user = setup.create_test_user()
        user_id = user.id

        # Call delete
        response = self.client.delete(
            f"{BASE_URL}{user_id}",
            headers=self.admin_auth_header)
        self.assertEqual(response.status_code, 200)

    # <-- PUT test needs to be debugged -->

    # def test_update_user_as_admin(self):
    #     # Create a user
    #     response = self.client.post(
    #         f"{BASE_URL}",
    #         headers=self.admin_auth_header,
    #         json=self.user_payload)

    #     user = response.get_json()
    #     user_id = user["id"]

    #     # Update payload
    #     self.user_payload["first_name"] = "Jack"
    #     self.user_payload["last_name"] = "Doe"
    #     self.user_payload["email"] = "changed@email.com"

    #     update_response = self.client.put(
    #         f"{BASE_URL}{user_id}",
    #         headers=self.admin_auth_header,
    #         json=self.user_payload
    #     )
    #     self.assertEqual(update_response.status_code, 200)
    #     updated = update_response.get_json()
    #     self.assertEqual(updated["first_name"], "Jack")

    def test_update_user_as_self(self):
        """ Can update first name and last name fields only """
        # Create a user
        user = setup.create_test_user()
        user_id = user.id
        user_token = setup.login(user)
        user_auth_header = {
            "Authorization": f'Bearer {user_token}'}

        # Construct limited payload
        user_payload = {
            "first_name": "Jack",
            "last_name": "Doe"
        }

        response = self.client.put(
            f"{BASE_URL}{user_id}",
            headers=user_auth_header,
            json=user_payload
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["first_name"], "Jack")

    # <-- This section covers successful GET requests -->

    def test_retrieve_all_users_empty_list(self):
        response = self.client.get(f"{BASE_URL}")
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertIsInstance(users, list)

    def test_retrieve_all_users(self):
        # Create a user
        response = self.client.post(
            f"{BASE_URL}",
            headers=self.admin_auth_header,
            json=self.user_payload)

        user = response.get_json()
        user_id = user["id"]

        # Fetch the user
        response = self.client.get(f"{BASE_URL}")
        self.assertEqual(response.status_code, 200)

        # Check the list is returned
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Check the list contains the place id
        user_ids = [u["id"] for u in data]
        self.assertIn(user_id, user_ids)

    def test_retrieve_specific_user(self):
        # Create a user
        response = self.client.post(
            f"{BASE_URL}",
            headers=self.admin_auth_header,
            json=self.user_payload)

        user = response.get_json()
        user_id = user["id"]

        # Fetch the user
        response = self.client.get(f"{BASE_URL}{user_id}")

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["first_name"], self.user_payload["first_name"])
        self.assertEqual(data["last_name"], self.user_payload["last_name"])
        self.assertEqual(data["email"], self.user_payload["email"])

    # <-- This section tests authorisation -->

    def test_create_user_invalid_email(self):
        self.user_payload["email"] = "fake"
        response = self.client.post(
            f"{BASE_URL}",
            headers=self.admin_auth_header,
            json=self.user_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid Email. Try again")

    # <-- This section tests validation scenarios -->

    def test_retrieve_non_existent_user(self):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = self.client.get(f"{BASE_URL}{fake_id}")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "User not found")

    def test_create_user_missing_field(self):
        unique_email = f"sarah_{uuid.uuid4().hex}@example.com"
        payload = {
            "last_name": "Sarah",
            "email": unique_email
        }
        response = self.client.post(f"{BASE_URL}", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("errors", data)
        self.assertIn("first_name", data["errors"])
        self.assertIn("required", data["errors"]["first_name"].lower())

    def test_update_email_as_self(self):
        # Create a user
        user = setup.create_test_user()
        user_id = user.id
        user_token = setup.login(user)
        user_auth_header = {
            "Authorization": f'Bearer {user_token}'}

        # Construct limited payload
        user_payload = {
            "first_name": "Jack",
            "last_name": "Doe",
            "email": "new@email.com"
        }

        print(self.user_payload)

        response = self.client.put(
            f"{BASE_URL}{user_id}",
            headers=user_auth_header,
            json=user_payload
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn(data["error"], "You cannot modify email or password")


if __name__ == "__main__":
    unittest.main()
