import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews')
        self.assertEqual(response.status_code, 200)

    def create_review(self):
        data = {
            "rating": 4,
            "comment": "Nice place!",
            "user_id": "1234",
            "place_id": "5678"
        }
        response = self.client.post('/api/v1/reviews', json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 4)


if __name__ == '__main__':
    unittest.main()
