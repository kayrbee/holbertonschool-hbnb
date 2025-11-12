import unittest
from unittest.mock import patch
from app.models.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        """Setup default valid user data for tests."""
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!",
            "is_admin": False
        }

    @patch('app.models.user.bcrypt.generate_password_hash')
    def test_user_initialization_valid(self, mock_hash):
        """Test creating a user with valid data."""
        mock_hash.return_value.decode.return_value = "hashed_pw"
        user = User(**self.valid_data)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.password, "hashed_pw")
        self.assertFalse(user.is_admin)

    def test_first_name_validation(self):
        """Test first_name validation rules."""
        data = self.valid_data.copy()
        data['first_name'] = ""  # empty first name
        with self.assertRaises(TypeError):
            User(**data)

        data['first_name'] = "A" * 51  # too long
        with self.assertRaises(ValueError):
            User(**data)

        data['first_name'] = 123  # not string
        with self.assertRaises(TypeError):
            User(**data)

    def test_last_name_validation(self):
        """Test last_name validation rules."""
        data = self.valid_data.copy()
        data['last_name'] = ""
        with self.assertRaises(TypeError):
            User(**data)

        data['last_name'] = "B" * 51
        with self.assertRaises(ValueError):
            User(**data)

        data['last_name'] = 456
        with self.assertRaises(TypeError):
            User(**data)

    def test_email_validation(self):
        """Test email validation rules."""
        data = self.valid_data.copy()
        data['email'] = ""
        with self.assertRaises(TypeError):
            User(**data)

        data['email'] = "invalid-email"
        with self.assertRaises(ValueError):
            User(**data)

        data['email'] = 123
        with self.assertRaises(TypeError):
            User(**data)

    def test_is_email_valid_method(self):
        """Test the is_email_valid helper method."""
        user = User(**self.valid_data)
        self.assertTrue(user.is_email_valid("test@example.com"))
        self.assertFalse(user.is_email_valid("invalid-email"))
        self.assertFalse(user.is_email_valid("bad@domain"))

    @patch('app.models.user.bcrypt.generate_password_hash')
    @patch('app.models.user.bcrypt.check_password_hash')
    def test_password_hash_and_verify(self, mock_check, mock_hash):
        """Test password hashing and verification."""
        mock_hash.return_value.decode.return_value = "hashed_pw"
        mock_check.return_value = True

        user = User(**self.valid_data)
        self.assertEqual(user.password, "hashed_pw")
        self.assertTrue(user.verify_password("SecurePass123!"))
        mock_check.assert_called_with("hashed_pw", "SecurePass123!")

    def test_to_dict(self):
        """Test the to_dict method returns correct dictionary."""
        with patch('app.models.user.bcrypt.generate_password_hash') as mock_hash:
            mock_hash.return_value.decode.return_value = "hashed_pw"
            user = User(**self.valid_data)
            user.id = 1  # simulate database ID
            result = user.to_dict()
            expected = {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "is_admin": False
            }
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
