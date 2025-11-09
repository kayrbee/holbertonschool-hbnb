import pytest
from app.models.user import User


def test_explicit_nonadmin_user_creation():
    mary = User("Mary", "Smith", "mary.smith@example.com",
                "password123", False)
    assert mary.first_name == "Mary"
    assert mary.last_name == "Smith"
    assert mary.email == "mary.smith@example.com"
    assert mary.is_admin == False
    assert mary.verify_password("password123") == True


def test_implicit_nonadmin_user_creation():
    michael = User("Michael", "Mandy",
                   "michael.mandy@example.com", "password123")
    assert michael.first_name == "Michael"
    assert michael.last_name == "Mandy"
    assert michael.email == "michael.mandy@example.com"
    assert michael.verify_password("password123") == True


def test_admin_user_creation():
    bob = User("Robert", "Smith", "robert.smith@example.com",
               "password123", True)
    assert bob.first_name == "Robert"
    assert bob.last_name == "Smith"
    assert bob.email == "robert.smith@example.com"
    assert bob.is_admin == True
    assert bob.verify_password("password123") == True


def test_first_name_must_be_provided():
    with pytest.raises(TypeError) as exc_info:
        User(first_name=None, last_name="Smith",
             email="a@a.com", password="password")
    assert str(exc_info.value) == "First name must be provided"


def test_first_name_must_be_string():
    with pytest.raises(TypeError) as exc_info:
        User(first_name=123, last_name="Smith",
             email="a@a.com", password="password")
    assert str(exc_info.value) == "First name must be a string"


def test_first_name_must_be_less_than_50chars():
    with pytest.raises(ValueError) as exc_info:
        User(first_name="Cordelia Michele Applegate Genevieve Wagner The Third", last_name="Smith",
             email="a@a.com", password="password")
    assert str(exc_info.value) == "First name cannot exceed 50 characters"


def test_last_name_must_be_provided():
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Sarah", last_name=None,
             email="a@a.com", password="password")
    assert str(exc_info.value) == "Last name must be provided"


def test_last_name_must_be_less_than_50chars():
    with pytest.raises(ValueError) as exc_info:
        User(first_name="Cordelia", last_name="Cordelia Michele Applegate Genevieve Wagner The Third Smith",
             email="a@a.com", password="password")
    assert str(exc_info.value) == "Last name cannot exceed 50 characters"


def test_last_name_must_be_string():
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Sarah", last_name=123,
             email="a@a.com", password="password")
    assert str(exc_info.value) == "Last name must be a string"


def test_email_must_be_provided():
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Sarah", last_name="Smith",
             email=None, password="password")
    assert str(exc_info.value) == "Email must be provided"


def test_email_must_be_string():
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Sarah", last_name="Smith",
             email=123, password="password")
    assert str(exc_info.value) == "Email must be a string"


def test_password_must_be_provided():
    with pytest.raises(TypeError) as exc_info:
        User(first_name="Sarah", last_name="Smith",
             email="a@a.com", password=None)
    assert str(exc_info.value) == "Password must be provided"
