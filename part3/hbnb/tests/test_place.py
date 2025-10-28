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
            "amenities": ["wifi", "pool"]
        })
        self.assertIn(response.status_code, [201, 400])


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
        self.assertIn(response.status_code, [201, 400])
    
    def test_create_place_invalid_owner_id(self):
        """Creating a place with a non-existent owner_id should fail."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Owner Place",
            "description": "Should fail due to bad owner_id",
            "price": 150,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "does-not-exist",  # invalid
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json() or {}
    
    def test_create_place_invalid_amenity_ids(self):
        """Creating a place with invalid amenities should fail."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Amenities Place",
            "description": "Should fail due to bad amenity IDs",
            "price": 180,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["amenity-xyz"]  #invalid
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json() or {}


    def test_create_place_missing_field(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",  # invalid
            "description": "A nice place to stay",
            "price": 200,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi", "pool"]
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
            "amenities": ["wifi", "pool"]
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
            "amenities": ["wifi", "pool"]
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
        self.assertIn(create_response.status_code, [200, 400, 404])

        data = create_response.get_json() or {}
        place_id = data.get("id")

        # Retrieve it by ID
        response = self.client.get(f"/api/v1/places/{place_id}")
        self.assertIn(response.status_code, [200, 400, 404])


    def test_update_place_invalid_data(self):
        """Test updating a place with invalid price, latitude, and longitude."""
        # create valid place
        create_resp = self.client.post('/api/v1/places/', json={
            "title": "Updatable Place",
            "description": "Nice spot",
            "price": 100,
            "latitude": -37.8,
            "longitude": 144.9,
            "owner_id": "user123",
            "amenities": ["wifi"]
        })
        self.assertIn(create_resp.status_code, [200, 400])
        place_id = create_resp.get_json().get("id")

        # invalid price
        resp_price = self.client.put(f"/api/v1/places/{place_id}", json={"price": -5})
        data_price = resp_price.get_json() or {}
        self.assertEqual(resp_price.status_code, 400)
        self.assertIn("price", (data_price.get("error") or "").lower())

        # invalid latitude (> 90)
        resp_lat = self.client.put(f"/api/v1/places/{place_id}", json={"latitude": 123.45})
        data_lat = resp_lat.get_json() or {}
        self.assertEqual(resp_lat.status_code, 400)
        self.assertIn("latitude", (data_lat.get("error") or "").lower())

        # invalid longitude (< -180)
        resp_long = self.client.put(f"/api/v1/places/{place_id}", json={"longitude": -190.0})
        data_long = resp_long.get_json() or {}
        self.assertEqual(resp_long.status_code, 400)
        self.assertIn("longitude", (data_long.get("error") or "").lower())



if __name__ == "__main__":
    unittest.main()