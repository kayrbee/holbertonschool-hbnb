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
        
        #only update allowed fields 
        allowed_fields = ["first_name", "last_name", "is_admin"]
        for field in allowed_fields:
            if field in new_data:
                setattr(user, field, new_data[field])
                
        return user

    # --- Place ---
    def create_place(self, place_data, owner_id):
        """
        Create a place with including validation
        for price, latitude, and longitude
        """

        # Required fields
        required = ["title", "price", "latitude", "longitude", "amenities"]
        missing = [f for f in required if f not in place_data]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        # Validate owner exists
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id: user does not exist")

        description = place_data.get("description", "")
        new_place = Place(
            title=place_data["title"],
            description=description,
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            amenities=place_data["amenities"],
            owner_id=owner_id
        )
        self.place_repo.add(new_place)
        
        return new_place

        # Validate numeric ranges
        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")
        if price is None or price < 0:
            raise ValueError("Price must be a non-negative number")
        if latitude is None or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is None or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        # Normalise amenities to list[str]
        amenities = place_data.get("amenities", [])
        if isinstance(amenities, str):
            amenities = [amenities]
        if not isinstance(amenities, list):
            raise ValueError("Amenities must be a list of amenity IDs")

        # Validate amenities exist
        valid_amenity_ids = []
        for amenity_id in amenities:
            if not self.amenity_repo.get(amenity_id):
                raise ValueError(f"Invalid amenity_id: {amenity_id} does not exist")
            valid_amenity_ids.append(amenity_id)

        init_args = {
            "title": place_data["title"],
            "description": place_data.get("description", ""),
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner_id": owner_id,
            "amenities": valid_amenity_ids,
            "reviews": place_data.get("reviews", []),
        }

        place = Place(**init_args)
        self.place_repo.add(place)
        return place

    def get_place_by_id(self, place_id):
        """Get a place by ID"""
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        if not self.place_repo.get_all():
            raise ValueError("No Places found")
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place by ID"""

        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError("Place not found")

        updates = place_data

        if "price" in updates and updates["price"] is not None:
            if updates["price"] < 0:
                raise ValueError("Price must be a positive number")

        if "latitude" in updates and updates["latitude"] is not None:
            if not (-90 <= updates["latitude"] <= 90):
                raise ValueError("Latitude must be between -90 and 90")

        if "longitude" in updates and updates["longitude"] is not None:
            if not (-180 <= updates["longitude"] <= 180):
                raise ValueError("Longitude must be between -180 and 180")

        if "amenities" in updates:
            amenities = updates["amenities"]

            # allow string or list
            if isinstance(amenities, str):
                amenities = [amenities]

            if not isinstance(amenities, list):
                raise ValueError("Amenities must be a list of amenity IDs")

            # Verify each amenity ID exists in the repository
            for amenity_id in amenities:
                if not self.amenity_repo.get(amenity_id):
                    raise ValueError(f"Invalid amenity_id: {amenity_id} does not exist")

            # Replace the original value with the cleaned list
            updates["amenities"] = amenities

        allowed = {"title", "description", "price", "latitude", "longitude", "amenities"}

        # new dictionary containing only valid update keys
        safe_updates = {}
        for key, value in updates.items():
            if key in allowed:
                safe_updates[key] = value

        self.place_repo.update(place_id, safe_updates)

        return self.place_repo.get(place_id)

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
        review.update(data)
        return review

    def get_review_by_user_and_place(self, user_id, place_id):
        reviews = self.get_reviews_by_place(place_id)
        for r in reviews:
            if hasattr(r, "user") and str(r.user) == str(user_id):
                return r
        if isinstance(r, dict) and str(r.get("user")) == str(user_id):
            return r
        return None

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
