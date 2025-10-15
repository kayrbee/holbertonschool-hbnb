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

    # --- Place ---
    def create_place(self, place_data):
        """
        Create a place with including validation
        for price, latitude, and longitude
        """
        # Validation
        if "price" not in place_data or place_data["price"] < 0:
            raise ValueError("Price must be a positive number")
        if "latitude" not in place_data or not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if "longitude" not in place_data or not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        # Create and save the place
        place = Place(**place_data)
        self.place_repo.create(place)
        return place.to_dict()
    
    def get_place(self, place_id):
        """Get a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.to_dict()

    def get_all_places(self):
        """Get all places"""
        places = self.place_repo.all()
        
        place_dicts = []
        for p in places:
            place_dicts.append(p.to_dict())

        return place_dicts

    def update_place(self, place_id, place_data):
        """Update a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)

        self.place_repo.update(place_id, place)
        return place.to_dict()
    
    # --- Amenity ---
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
