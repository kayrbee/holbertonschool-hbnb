import unittest
from app import create_app, db
from config import TestConfig
from flask_jwt_extended import decode_token


def create_test_admin_helper():
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
        self.admin = create_test_admin_helper()

        # Construct a valid login dataset
        self.valid_auth_data = {
            "email": self.admin.email,
            "password": "password"
        }

    # Teardown is only necessary with a persistent test db
    # - the test config is currently using: memory:

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_valid_login(self):
        """ Post to /login endpoint with correct email and correct password of
        an existing user """
        response = self.client.post(
            "/api/v1/auth/login",
            json=self.valid_auth_data,
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


if __name__ == '__main__':
    unittest.main()
