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

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

# validate property fields. if fields don't have entries