import unittest
import json
import uuid
from app import create_app, db
from config import TestConfig
import tests.helper_methods as setup
from flask_jwt_extended import decode_token


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """ Set up before each test """
        # Create a fresh app and db before each test
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.app.testing = True
        self.client = self.app.test_client()

        # Create a reviewer & jwt token
        self.reviewer = setup.create_test_user()
        self.reviewer_id = self.reviewer.id
        self.reviewer_token = setup.login(self.reviewer)
        self.reviewer_auth_header = {
            "Authorization": f"Bearer {self.reviewer_token}"}

        # Create a place owner
        self.owner = setup.create_test_user()
        self.owner_id = self.owner.id
        self.owner_token = setup.login(self.owner)
        self.owner_auth_headers = {
            "Authorization": f"Bearer {self.owner_token}"}

        # Create a place to review
        self.place = setup.create_place(self.owner_id)
        self.place_id = self.place.id

        # Dummy review data (valid)
        self.review_data = {
            "text": "A lovely place",
            "rating": 5,
            "user": self.reviewer_id,
            "place": self.place_id
        }

    def test_get_reviews_empty_list(self):
        """ Get reviews should return an empty list when there are no reviews
        """
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_create_review_success(self):
        """ POST /api/v1/reviews/ should create a review - reviewer cannot be owner """
        response = self.client.post(
            "/api/v1/reviews/",
            headers=self.reviewer_auth_header,
            json=self.review_data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], self.review_data["text"])
        self.review_id = data["id"]

    def test_create_review_with_missing_rating(self):
        """POST /api/v1/reviews should fail with missing field"""
        self.review_data["rating"] = None

        response = self.client.post(
            "/api/v1/reviews/",
            headers=self.reviewer_auth_header,
            json=self.review_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("errors", data)
        self.assertIn("rating", data["errors"])

    def test_get_all_reviews_with_one_review_in_list(self):
        """GET /api/v1/reviews/ should return a list of reviews"""
        # Create a review to return
        review = setup.create_review(self.place_id, self.reviewer_id)

        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Check that there's data in the list
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        #  Check that the review_id is in the returned data
        review_texts = [r["id"] for r in data]
        self.assertIn(review.id, review_texts)

    def test_get_review_by_id(self):
        """GET /api/v1/reviews/<id> should return the review <id> """
        # Pre-condition - create review & save its id
        review = setup.create_review(self.place_id, self.reviewer_id)

        get_resp = self.client.get(f"/api/v1/reviews/{review.id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.get_json()["id"], review.id)

    def test_update_review_as_reviewer(self):
        """PUT /api/v1/reviews/<id> should update the review"""
        # Create a review
        review = setup.create_review(self.place_id, self.reviewer_id)
        review_id = review.id

        # Update the review data
        self.review_data["rating"] = 1
        self.review_data["text"] = "Updated review text"
        # print("Created review:", review.to_dict())
        # print("PUT payload:", self.review_data)
        # print("Current user from auth header:",
        #       decode_token(self.reviewer_token)["sub"])
        # print("review_id", review_id, "user: ",
        #       self.reviewer_id, "place:", self.place_id)

        response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            headers=self.reviewer_auth_header,
            json=self.review_data,
            content_type="application/json"
        )
        # Handy debugging statement!
        print(response.status_code, response.get_json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["text"], "Updated review text")
        self.assertEqual(response.get_json()["rating"], 1)

    def test_delete_review(self):
        """DELETE /api/v1/reviews/<id> should delete the review <id>"""
        # create a review
        review = setup.create_review(self.place_id, self.reviewer_id)
        review_id = review.id

        del_resp = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self.reviewer_auth_header,
        )
        self.assertEqual(del_resp.status_code, 200)

        get_resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(get_resp.status_code, 404)

    def test_get_reviews_by_place(self):
        """GET /api/v1/reviews/places/<place_id>/reviews should return reviews"""
        review = setup.create_review(self.place_id, self.reviewer_id)
        print(review)

        response = self.client.get(
            f"/api/v1/reviews/places/{self.place_id}/reviews")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)


if __name__ == '__main__':
    unittest.main()
