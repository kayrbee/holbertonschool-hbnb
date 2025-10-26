#!/usr/bin/python3
import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
   
    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_too_long(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Aesop hand wash from the himalayas with plastic microbeads, which noone wants"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_not_string(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": 1586813485
        })
        self.assertEqual(response.status_code, 400)

    #   TO DO: empty handling
    # def test_create_empty_amenity(self):
    #     response = self.client.post('/api/v1/amenities/', json={
    #         "name": ""
    #     })
    #     self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()

