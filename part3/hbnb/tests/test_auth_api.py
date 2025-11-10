import unittest
from app import create_app, db
from config import TestConfig
from flask_jwt_extended import decode_token


def create_test_admin():
    from app.models import User
    admin = User(first_name="Mary", last_name="Admin",
                 email="mary1@admin.com", password="password", is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return admin


class TestAuthEndpoints(unittest.TestCase):

    def setUp(self):
        """ Set up before each test """
        # Create a fresh app and db before each test
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.app.testing = True
        self.client = self.app.test_client()

        # Create test user before the test runs - user must exist
        self.admin = create_test_admin()

        # Construct a valid login data set & modify as needed
        self.auth_data = {
            "email": self.admin.email,
            "password": "password"
        }

    # The test config is currently using an in-memory test db
    # Teardown is only necessary with a persistent test db
    # Left here for future reference

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_valid_login(self):
        """ Post to /login endpoint with correct email and correct password of
        an existing user """
        response = self.client.post(
            "/api/v1/auth/login",
            json=self.auth_data,
            content_type="application/json"
        )

        # Assert status code
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Assert that access_token is in response
        self.assertIn("access_token", data)

        # Fetch the token from response data
        access_token = data["access_token"]

        # Decode the token
        decoded_token = decode_token(access_token)

        # Assert that jwt subject matches user_id
        self.assertEqual(decoded_token["sub"], self.admin.id)

    def test_login_with_invalid_password(self):
        self.auth_data["password"] = "wrongpassword"
        response = self.client.post(
            "/api/v1/auth/login",
            json=self.auth_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)

        data = response.get_json()
        self.assertEqual(data, {'error': 'Invalid credentials'})

    def test_login_with_invalid_email(self):
        self.auth_data["email"] = "fake@example.com"
        response = self.client.post(
            "/api/v1/auth/login",
            json=self.auth_data,
            content_type="application/json"
        )

        # Check error code
        self.assertEqual(response.status_code, 401)

        data = response.get_json()

        # Check that no jwt generated
        self.assertNotIn("access_token", data)

        # Check response message
        self.assertEqual(data, {'error': 'Invalid credentials'})


if __name__ == '__main__':
    unittest.main()
