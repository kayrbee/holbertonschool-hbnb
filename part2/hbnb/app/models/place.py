from app.models.base_class import Base

class Place(Base):
    def __init__(
            self,
            title: str,
            description: str,
            price: float,
            latitude: float,
            longitude: float,
            owner=False
        ):
        super().__init__()
        self.title = self.validate_non_empty(title, "title")
        self.description = self.validate_non_empty(description, "description")
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
    
    # --- Validation methods ---
    def validate_non_empty(self, value, field_name):
        """Ensure the field has a non-empty value."""
        if not value:
            raise ValueError("{} cannot be empty.".format(field_name))
        return value
    
    def validate_price(self, value):
        """Ensure price is a positive number."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number.")
        return value
    
    def validate_latitude(self, value):
        """Ensure latitude is between -90 and 90."""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return value
    
    def validate_longitude(self, value):
        """Ensure longitude is between -180 and 180."""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return value
