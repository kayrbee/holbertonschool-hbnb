import unittest
import json
import uuid
from app import create_app
from flask_jwt_extended import decode_token


class TestAuthEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Create test data
        # Pre-condition for successful_login - User must exist
        # Create a valid user_email
        unique_email = f"test_{uuid.uuid4().hex}@example.com"
        password = "password123"
        user_response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": unique_email,
                "password": password
            }
        )
        self.assertEqual(user_response.status_code, 201)
        self.email = unique_email
        self.password = password
        self.user_id = user_response.get_json()["id"]

        # Construct a valid login dataset
        self.valid_auth_data = {
            "email": self.email,
            "password": self.password
        }

    def test_valid_login(self):
        """ Post to /login endpoint with correct email and correct password of
        an existing user """
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.valid_auth_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Assert that access_token is in response
        self.assertIn("access_token", data)

        # Fetch the token from response data
        access_token = data["access_token"]

        # app_context() pushes an application context for the duration of the block,
        # which means that decode_token can now access current_app.config["JWT_SECRET_KEY"]
        # and other config values. This is required in tests because
        # self.client only pushes a request context -
        # self.client does not push an application context outside of request handling.
        with self.app.app_context():
            from flask_jwt_extended import decode_token
            # Decode the token
            decoded_token = decode_token(access_token)

            # Assert that jwt subject matches user_id
            self.assertEqual(decoded_token["sub"], self.user_id)
