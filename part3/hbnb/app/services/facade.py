#!/usr/bin/python3

from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import uuid


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # User
    def create_user(self, user_data):
        """ create a new user (POST /users)"""
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user_by_id(self, user_id):
        """ retrieve a user by ID (GET /users/<user_id>)"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """ retrieve a user by email address (GET /users/email/<email_address>) """
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """ list all users that exist (GET /users)"""
        return self.user_repo.get_all()

    def put_user(self, user_id, new_data):
        """ update existing user's information (PUT /users/<user_id>)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.update(new_data)
        return user

    def delete_user(self, user_id):
        """ Delete a user """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.delete(user_id)

    # --- Place ---
    def create_place(self, place_data, owner_id):
        """
        Create a place with including validation
        for price, latitude, and longitude
        """
        # Amenities to List
        amenities = place_data.get("amenities", [])
        
        if isinstance(amenities, str):
            amenities = [a.strip() for a in amenities.split(",") if a.strip()]
        elif not isinstance(amenities, list):
            raise ValueError("Amenities must be a list of amenity IDs")
        
        place_data["amenities"] = amenities

        # Validate owner exists
        owner = self.user_repo.get(place_data.get("owner_id"))          # Additional layer of validation
        if not owner:
            raise ValueError("Invalid owner_id: user does not exist")

        # Convert amenity IDs from payload into Amenity model instances
        raw_amenities = place_data.get("amenities", [])
        if not isinstance(raw_amenities, list):
            raise ValueError("Amenities must be a list of amenity IDs")

        valid_amenities = []
        for amenity_id in raw_amenities:
            if not amenity_id or not isinstance(amenity_id, str):
                continue  # skip invalid entries

            amenity = self.amenity_repo.get(amenity_id)                 # Links the payload ID with the repo ID
            if not isinstance(amenity, Amenity):                        # Validates existing ID
                raise ValueError(f"Amenity ID {amenity_id} not found")
            valid_amenities.append(amenity)                             # Build list of valid Amenity model instances

        # Create place
        new_place = Place(
            title=str(place_data["title"]),
            description=place_data.get("description", ""),
            price=float(place_data["price"]),
            latitude=float(place_data["latitude"]),
            longitude=float(place_data["longitude"]),
            owner_id=str(owner_id),
            amenities=valid_amenities
        )

        # Save and return
        self.place_repo.add(new_place)
        return new_place

    def get_place_by_id(self, place_id):
        """Get a place by ID"""
        if not self.place_repo.get(place_id):
            raise LookupError("Place not found")
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError("Place not found")
        
        # Update allowed fields
        allowed = {"title", "description", "price", "latitude", "longitude", "amenities"}
        for key, value in place_data.items():
            if key in allowed:
                setattr(place, key, value)
        
        self.place_repo.update(place)
        return place

    def delete_place(self, place_id):
        """ Deletes a place """
        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError("Place not found")
        self.place_repo.delete(place_id)

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
        try:
            uuid.UUID(amenity_id)
        except ValueError:
            raise ValueError('Amenity ID must be a valid UUID, not a name')

        existing = self.amenity_repo.get(amenity_id)
        if existing is None:
            raise ValueError("Amenity not found")

        return existing

    def get_all_amenities(self):
        """
        Retrieves amenity list or returns
        empty list if none exist
        """
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

    def delete_amenity(self, amenity_id):
        """
        Deletes an existing amenity
        nb - sql delete doesn't return rows
        which means there's no return value from a delete()
        """
        if not self.amenity_repo.get(amenity_id):
            raise ValueError("Amenity not found")
        self.amenity_repo.delete(amenity_id)

    # --- Reviews ---
    def create_review(self, review_data):
        """ create a new review (POST /reviews)"""
        review = Review(**review_data)
        # Validate user and place before saving review
        place = self.place_repo.get(review.place_id)
        user = self.user_repo.get(review.user_id)
        if not place:
            raise ValueError("Place not found, cannot submit review")
        if not user:
            raise ValueError("User not found, cannot submit review")
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        if not self.review_repo.get(review_id):
            raise ValueError("Review not found")
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        review.update(data)
        return review

    def get_review_by_user_and_place(self, user_id, place_id):
        reviews = self.get_reviews_by_place(place_id)
        for r in reviews:
            if hasattr(r, "user") and r.user == user_id:
                return r
            if isinstance(r, dict) and r.get("user") == user_id:
                return r
        return None

    def delete_review(self, review_id):
        """ 
        Delete a review

        Note: the 404 validation check was
        removed because it duplicated logic at the API layer and resulted
        in an extra, unnecessary db call.

        I chose to keep the 404 validation at the API layer for reviews
        because it was already necessary to call the db to perform an
        authorisation check on review owner

        """
        self.review_repo.delete(review_id)
