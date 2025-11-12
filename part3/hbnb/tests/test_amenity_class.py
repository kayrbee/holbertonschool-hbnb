import unittest
from datetime import datetime
from app import create_app, db
from config import TestConfig
from app.models.amenity import Amenity


class TestAmenityModel(unittest.TestCase):

    def setUp(self):
        """Create a fresh test database before each test."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    # --- Tests start here ---

    def test_create_amenity_valid_name(self):
        """Test that a valid amenity can be created and stored."""
        amenity = Amenity(name="Pool")
        db.session.add(amenity)
        db.session.commit()

        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.name, "Pool")

    def test_name_must_be_string(self):
        """Test that amenity name must be a string."""
        with self.assertRaises(TypeError):
            Amenity(name=123)

    def test_name_length_limit(self):
        """Test that amenity name cannot exceed 50 characters."""
        long_name = "a" * 51
        with self.assertRaises(ValueError):
            Amenity(name=long_name)

    def test_to_dict_returns_expected_keys(self):
        """Test the to_dict() method returns expected structure."""
        amenity = Amenity(name="WiFi")
        db.session.add(amenity)
        db.session.commit()

        data = amenity.to_dict()

        # Ensure all expected keys are present
        self.assertIn("id", data)
        self.assertIn("name", data)

        # Ensure field types are correct
        self.assertIsInstance(data["id"], str)
        self.assertEqual(data["name"], "WiFi")

    def test_created_and_updated_timestamps_exist(self):
        """Ensure timestamps are automatically set by Base class."""
        amenity = Amenity(name="Gym")
        db.session.add(amenity)
        db.session.commit()

        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)


if __name__ == '__main__':
    unittest.main()
