#!/usr/bin/python3
import unittest
from app import create_app, db
from config import TestConfig
import tests.helper_methods as setup


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        """ Set up before each test """
        # Create a fresh app and db before each test
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.app.testing = True
        self.client = self.app.test_client()

        # Create an admin and a non-admin to test amenity creation
        self.admin = setup.create_test_user(is_admin=True)

        # Create a valid admin jwt
        self.admin_token = setup.login(self.admin)

        # Create auth header
        self.admin_auth_header = {
            "Authorization": f"Bearer {self.admin_token}"}

        # Create a non-admin user to test protected endpoints
        self.non_admin = setup.create_test_user()

        #  Create a valid non-admin jwt
        self.user_token = setup.login(self.non_admin)

        # Create auth header
        self.user_auth_header = {
            "Authorization": f"Bearer {self.user_token}"}

    # --- Tests start here ---

    def test_create_amenity_as_admin(self):
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_as_non_admin(self):
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.user_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_create_amenity_too_long(self):
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Aesop hand wash from the himalayas with plastic microbeads, which noone wants"})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_not_string(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": 1586813485
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_empty_name(self):
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": None})
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        # First, create an amenity to return
        self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_id(self):
        # First, create an amenity to return
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        amenity = response.get_json()
        amenity_id = amenity["id"]

        # Pass the amenity_id to the endpoint for testing
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_modify_amenity_as_admin(self):
        # First, create an amenity to modify
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        amenity = response.get_json()
        amenity_id = amenity["id"]

        # Pass the amenity_id to the endpoint for testing
        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            headers=self.admin_auth_header,
            json={"name": "Spa"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Spa")

    def test_delete_amenity_as_admin(self):
        # First, create an amenity to delete
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        amenity = response.get_json()
        amenity_id = amenity["id"]

        # Pass the amenity_id to the endpoint for testing
        response = self.client.delete(
            f'/api/v1/amenities/{amenity_id}',
            headers=self.admin_auth_header
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_amenity_as_non_admin(self):
        # First, create an amenity to delete
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.admin_auth_header,
            json={"name": "Pool"},
            content_type="application/json"
        )
        amenity = response.get_json()
        amenity_id = amenity["id"]

        # Pass the amenity_id to the endpoint for testing
        response = self.client.delete(
            f'/api/v1/amenities/{amenity_id}',
            headers=self.user_auth_header
        )
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
