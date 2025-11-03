import unittest
import json
import uuid
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Create test data
        # Pre-condition for create_review - User must exist
        # Create a valid user_id
        unique_email = f"test_{uuid.uuid4().hex}@example.com"
        user_response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": unique_email,
                "password": "password123"
            }
        )
        self.assertEqual(user_response.status_code, 201)
        self.user_id = user_response.get_json()["id"]

        # Pre-condition for create_review - Place must exist
        # Create a valid place_id
        place_response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Test Place",
                "description": "Test description",
                "latitude": 0.0,
                "longitude": 0.0,
                "price": 100,
                "owner_id": self.user_id,
                "reviews": [],
                "amenities": []
            }
        )
        self.assertEqual(place_response.status_code, 201)
        self.place_id = place_response.get_json()["id"]
        # Dummy review data (valid)
        self.review_data = {
            "text": "A lovely place",
            "rating": 5,
            "user": self.user_id,
            "place": self.place_id
        }

    def test_get_reviews_empty_list(self):
        """ Get reviews should return an empty list when there are no reviews
        Note: currently failing because test run order is not guaranteed
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_create_review_success(self):
        """POST /api/v1/reviews/ should create a review"""
        response = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps(self.review_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], self.review_data["text"])
        self.review_id = data["id"]

    def test_create_review_missing_field(self):
        """POST /api/v1/reviews should fail with missing field"""
        bad_data = self.review_data.copy()
        del bad_data["rating"]

        response = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps(bad_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_all_reviews(self):
        """GET /api/v1/reviews/ should return a list of reviews"""
        # Create a review first
        self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")

        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_all_reviews(self):
        """GET /api/v1/reviews should return a list"""
        # Create a review first
        self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")

        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_review_by_id(self):
        """GET /api/v1/reviews/<id> should return the review <id>"""
        post_resp = self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")
        review_id = post_resp.get_json()["id"]

        get_resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.get_json()["id"], review_id)

    def test_update_review(self):
        """PUT /api/v1/reviews/<id> should update the review"""
        # Create a review
        post_resp = self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")
        review_id = post_resp.get_json()["id"]

        updated_data = {
            "text": "Updated review",
            "rating": 4,
            "user": "user-123",
            "place": "place-456"
        }

        put_resp = self.client.put(
            f"/api/v1/reviews/{review_id}", data=json.dumps(updated_data), content_type="application/json")
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.get_json()["text"], "Updated review")
        self.assertEqual(put_resp.get_json()["rating"], 4)

    def test_delete_review(self):
        """DELETE /api/v1/reviews/<id> should delete the review <id>"""
        post_resp = self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")
        review_id = post_resp.get_json()["id"]

        del_resp = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(del_resp.status_code, 200)

        get_resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(get_resp.status_code, 404)

    def test_get_reviews_by_place(self):
        """GET /api/v1/reviews/places/<place_id>/reviews should return reviews"""
        self.client.post(
            "/api/v1/reviews/", data=json.dumps(self.review_data), content_type="application/json")

        response = self.client.get(
            f"/api/v1/reviews/places/{self.review_data['place']}/reviews")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)


if __name__ == '__main__':
    unittest.main()
