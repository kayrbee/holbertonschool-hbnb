import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A nice place to stay",
            "price": 200,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi, pool"]
        })
        self.assertEqual(response.status_code, 201)


    def test_create_place_empty_description(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "",
            "price": 200,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi, pool"]
        })
        self.assertEqual(response.status_code, 201)


    def test_create_place_missing_field(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",  # invalid
            "description": "A nice place to stay",
            "price": 200,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi, pool"]
        })
        self.assertEqual(response.status_code, 400)


    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A nice place to stay",
            "price": -200,  # invalid
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi, pool"]
        })
        self.assertEqual(response.status_code, 400)
    

    def test_create_place_invalid_coordinates(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A nice place to stay",
            "price": -200,
            "latitude": 100,  #invalid
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi, pool"]
        })
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_place_by_id(self):
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Testing single place retrieval",
            "price": 200,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi"]
        })
        self.assertEqual(create_response.status_code, 201)

        # Get the ID from the response
        place_id = create_response.get_json()["id"]

        # Retrieve it by ID
        response = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()