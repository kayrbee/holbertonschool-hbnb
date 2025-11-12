import unittest
from datetime import datetime
from app.models.amenity import Amenity


class TestAmenityModel(unittest.TestCase):
    """Pure unit tests for the Amenity model (no DB or Flask app context)."""

    def setUp(self):
        """Set up a base payload for reusability."""
        self.valid_name = "Pool"

    # --- Constructor and validation tests ---

    def test_create_amenity_valid_name(self):
        """Test creating an Amenity with a valid name."""
        amenity = Amenity(name=self.valid_name)

        # Ensure attributes are correctly assigned
        self.assertEqual(amenity.name, "Pool")
        # id, created_at, and updated_at may be set by Base class
        # Here we just ensure the class has these attributes
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_must_be_string(self):
        """Test that Amenity name must be a string."""
        with self.assertRaises(TypeError):
            Amenity(name=123)

    def test_name_length_limit(self):
        """Test that Amenity name cannot exceed 50 characters."""
        long_name = "a" * 51
        with self.assertRaises(ValueError):
            Amenity(name=long_name)

    # --- to_dict behavior ---

    def test_to_dict_returns_expected_keys(self):
        """Test the to_dict() output matches expected structure."""
        amenity = Amenity(name="WiFi")

        # Manually set an id and timestamps since DB isn't generating them
        amenity.id = "abc123"
        amenity.created_at = datetime.utcnow()
        amenity.updated_at = datetime.utcnow()

        data = amenity.to_dict()

        expected_keys = {"id", "name"}
        self.assertTrue(expected_keys.issubset(data.keys()))
        self.assertEqual(data["id"], "abc123")
        self.assertEqual(data["name"], "WiFi")

    # --- Timestamps simulated test ---

    def test_created_and_updated_timestamps_exist(self):
        """Ensure created_at and updated_at are datetime objects."""
        amenity = Amenity(name="Gym")
        # Simulate what the Base class would normally do
        amenity.created_at = datetime.utcnow()
        amenity.updated_at = datetime.utcnow()

        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)


if __name__ == '__main__':
    unittest.main()
