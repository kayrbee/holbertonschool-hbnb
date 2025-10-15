#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User
    def create_user(self, user_data):
        """ create a new user (POST /users)"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user_by_id(self, user_id):
        """ retrieve a user by ID (GET /users/<user_id>)"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """ retrieve a user by email address (GET /users/email/<email_address>) """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """ list all users that exist (GET /users)"""
        return self.user_repo.get_all()

    def put_user(self, user_id, new_data):
        """ update existing user's information (PUT /users/<user_id>)"""
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(new_data)
        return user

    # Placeholder method for fetching a place by ID

    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    # Amenity
    def create_amenity(self, amenity_data):
        """
        Checks amenity ID and creates a new amenity
        if it doesn't exist
        """
        amenity = Amenity(**amenity_data)

        if not self.amenity_repo.get(amenity.id):
            self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieves amenity or returns error if it
        doesn't exist
        """
        existing = self.amenity_repo.get(amenity_id)

        if existing is None:
            raise ValueError("Amenity not found")
        return existing

    def get_all_amenities(self):
        """
        Retrieves amenity list or returns
        error if list is empty
        """
        if not self.amenity_repo.get_all():
            raise ValueError("No Amenities found")
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an existing amenity or returns
        error if id doesn't exist
        """
        if not self.amenity_repo.get(amenity_id):
            raise ValueError("Amenity not found")
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity_data
