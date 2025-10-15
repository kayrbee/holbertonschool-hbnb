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
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    # --- title ---
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty.")
        self._title = value

    # --- description ---
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value:
            raise ValueError("Description cannot be empty.")
        self._description = value

    # --- price ---
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number.")
        self._price = value

    # --- latitude ---
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = value

    # --- longitude ---
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = value

    # --- helper methods ---
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
