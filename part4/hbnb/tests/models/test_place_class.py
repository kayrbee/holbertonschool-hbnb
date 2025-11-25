import unittest
from app.models.place import Place

# Dummy relationship classes


class Amenity:
    def __init__(self, name):
        self.name = name
        self.id = "a1"

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class DummyReview:
    def __init__(self, content):
        self.content = content


class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        """Prepare a base valid payload for Place creation."""
        self.base_payload = {
            "title": "Mountain Cabin",
            "description": "A cozy place in the woods",
            "price": 120.0,
            "latitude": 45.0,
            "longitude": -122.0,
            "user_id": "user-1",
            "reviews": []
        }

    # --- Happy Path ---

    def test_create_place_valid_data(self):
        place = Place(**self.base_payload)
        self.assertEqual(place.title, "Mountain Cabin")
        self.assertEqual(place.price, 120.0)
        self.assertEqual(place.latitude, 45.0)
        self.assertEqual(place.longitude, -122.0)
        self.assertEqual(place.user_id, "user-1")
        self.assertEqual(place.description, "A cozy place in the woods")
        self.assertEqual(place.amenities, [])
        self.assertEqual(place.reviews, [])

    # --- Validation Tests ---
    def test_empty_title_raises_value_error(self):
        payload = self.base_payload.copy()
        payload["title"] = ""
        with self.assertRaises(ValueError):
            Place(**payload)

    def test_invalid_price_raises_value_error(self):
        payload = self.base_payload.copy()
        payload["price"] = -10
        with self.assertRaises(ValueError):
            Place(**payload)

        payload["price"] = "cheap"
        with self.assertRaises(ValueError):
            Place(**payload)

    def test_latitude_out_of_range(self):
        payload = self.base_payload.copy()
        payload["latitude"] = 100  # invalid
        with self.assertRaises(ValueError):
            Place(**payload)

    def test_longitude_out_of_range(self):
        payload = self.base_payload.copy()
        payload["longitude"] = 200  # invalid
        with self.assertRaises(ValueError):
            Place(**payload)

    def test_empty_user_id_raises(self):
        payload = self.base_payload.copy()
        payload["user_id"] = ""
        with self.assertRaises(ValueError):
            Place(**payload)

    # --- Relationship helpers ---

    def test_add_review_appends_to_list(self):
        place = Place(**self.base_payload)
        # The call to __dict__ is necessary to bypass SQLAlchemy's managed properties
        place.__dict__['reviews'] = []
        review = DummyReview("Great stay!")
        place.add_review(review)
        self.assertIn(review, place.reviews)

    def test_add_amenity_appends_to_list(self):
        place = Place(**self.base_payload)
        # Bypass SQLAlchemy-managed property
        place.__dict__['amenities'] = []
        amenity = Amenity("WiFi")
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)

    # --- to_dict behavior ---

    def test_to_dict_contains_expected_fields(self):
        amenity = Amenity("WiFi")
        place = Place(**self.base_payload)
        # Bypass SQLAlchemy-managed property
        place.__dict__['amenities'] = []
        # also bypass reviews to keep it consistent
        place.__dict__['reviews'] = []
        place.add_amenity(amenity)

        result = place.to_dict()

        # Basic structure
        expected_keys = {"id", "title", "description", "price", "latitude",
                         "longitude", "user", "amenities", "reviews"}
        self.assertTrue(expected_keys.issubset(result.keys()))
        self.assertIsInstance(result["amenities"], list)
        self.assertEqual(result["amenities"][0]["name"], "WiFi")
        self.assertEqual(result["reviews"], [])
        self.assertIn("user", result)

    def test_description_defaults_to_empty_string(self):
        payload = self.base_payload.copy()
        payload.pop("description")
        place = Place(**payload)
        self.assertEqual(place.description, "")


if __name__ == "__main__":
    unittest.main()
