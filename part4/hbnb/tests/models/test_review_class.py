import unittest
from datetime import datetime
from app.models.review import Review


class TestReviewModel(unittest.TestCase):
    """ Unit tests for the Review model """

    def setUp(self):
        """Prepare a valid payload for review creation."""
        self.valid_payload = {
            "rating": 5,
            "text": "Excellent stay!",
            "place": "place-123",
            "user": "user-456"
        }

    # --- Constructor & attribute tests ---

    def test_create_review_valid(self):
        """Test creating a Review with valid data."""
        review = Review(**self.valid_payload)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, "Excellent stay!")
        self.assertEqual(review.place_id, "place-123")
        self.assertEqual(review.user_id, "user-456")
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    # --- Validation tests ---

    def test_text_must_be_string_and_not_empty(self):
        """Text must be non-empty string."""
        with self.assertRaises(TypeError):
            Review(rating=5, text=123, place="place-1", user="user-1")
        with self.assertRaises(ValueError):
            Review(rating=5, text="   ", place="place-1", user="user-1")

    def test_rating_must_be_int_and_in_range(self):
        """Rating must be int between 1 and 5."""
        with self.assertRaises(TypeError):
            Review(rating="5", text="Good", place="place-1", user="user-1")
        with self.assertRaises(ValueError):
            Review(rating=0, text="Bad", place="place-1", user="user-1")
        with self.assertRaises(ValueError):
            Review(rating=6, text="Too high", place="place-1", user="user-1")

    def test_user_id_must_be_nonempty_string(self):
        """User must be a string UUID."""
        with self.assertRaises(ValueError):
            Review(rating=4, text="Nice", place="place-1", user="")
        with self.assertRaises(TypeError):
            Review(rating=4, text="Nice", place="place-1", user=123)

    def test_place_id_must_be_nonempty_string(self):
        """Place must be a string UUID."""
        with self.assertRaises(ValueError):
            Review(rating=4, text="Nice", place="", user="user-1")
        with self.assertRaises(TypeError):
            Review(rating=4, text="Nice", place=123, user="user-1")

    # --- Update method tests ---

    def test_update_changes_attributes(self):
        """update() modifies only changed fields and preserves others."""
        review = Review(**self.valid_payload)

        # Simulate timestamps
        review.updated_at = datetime.utcnow()

        old_updated_at = review.updated_at
        review.update({"rating": 3, "text": "Good stay"})
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.text, "Good stay")
        # If .save() updates updated_at, the value should change
        self.assertNotEqual(review.updated_at, old_updated_at)

    def test_update_does_not_change_if_value_same(self):
        """update() leaves attributes unchanged if value is the same."""
        review = Review(**self.valid_payload)
        old_rating = review.rating
        old_text = review.text
        old_updated_at = review.updated_at

        review.update({"rating": old_rating, "text": old_text})
        self.assertEqual(review.rating, old_rating)
        self.assertEqual(review.text, old_text)
        # updated_at still updated by save()
        self.assertNotEqual(review.updated_at, old_updated_at)

    # --- to_dict tests ---

    def test_to_dict_returns_expected_keys(self):
        """to_dict() returns all expected keys."""
        review = Review(**self.valid_payload)
        # Assign dummy id since no DB
        review.id = "rev-1"
        data = review.to_dict()
        expected_keys = {"id", "rating", "text", "user", "place"}
        self.assertTrue(expected_keys.issubset(data.keys()))
        self.assertEqual(data["id"], "rev-1")
        self.assertEqual(data["rating"], self.valid_payload["rating"])
        self.assertEqual(data["text"], self.valid_payload["text"])
        self.assertIsInstance(data["user"], dict)
        self.assertEqual(data["place"], self.valid_payload["place"])


if __name__ == "__main__":
    unittest.main()
