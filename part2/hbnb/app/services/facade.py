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

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass
    
    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
    pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
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
