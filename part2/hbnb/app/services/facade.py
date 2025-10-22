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
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.update(new_data)
        return user

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

        # Normalise amenities (string -> list)
        amenities = place_data.get("amenities", [])
        if isinstance(amenities, str):
            amenities = [amenities]

        # Args Place accepts
        init_args = {
            "title": place_data["title"],
            "description": place_data.get("description", ""),
            "price": place_data["price"],
            "latitude": place_data["latitude"],
            "longitude": place_data["longitude"],
            "owner_id": place_data["owner_id"],
            "amenities": amenities,
            "reviews": place_data.get("reviews", []),
        }

        # Create and save the place
        place = Place(**init_args)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place_by_id(self, place_id):
        """Get a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if isinstance(place, dict):
            return place
        return place.to_dict()

    def get_all_places(self):
        """Get all places"""
        places = self.place_repo.get_all()

        place_dicts = []
        for p in places:
            place_dicts.append(p.to_dict())

        return place_dicts

    def update_place(self, place_id, place_data):
        """Update a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

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

    # --- Reviews ---
    def create_review(self, review_data):
        """ create a new review (POST /reviews)"""
        review = Review(**review_data)
        # Validate user and place before saving review
        place = self.place_repo.get(review.place)
        user = self.user_repo.get(review.user)
        if not place:
            raise ValueError("Place not found, cannot submit review")
        if not user:
            raise ValueError("User not found, cannot submit review")
        self.review_repo.add(review)
        place.add_review(review.to_dict())
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
        try:
            review.update(data)
            return review
        except TypeError as e:
            return f"{e}"

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        place_id = review.place
        place = self.place_repo.get(place_id)
        # Remove this review from place's reviews list before deletion
        place.reviews = [r for r in place.reviews if r['id'] != review.id]
        self.review_repo.delete(review_id)
        return "Review deleted"
