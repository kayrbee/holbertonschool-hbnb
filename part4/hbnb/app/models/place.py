from app import db
from .base_class import Base
from sqlalchemy.orm import validates

""" Association table (keep at top pls)"""
place_amenity = db.Table('place_amenity',
                         db.Column('place_id', db.String(36), db.ForeignKey(
                             'places.id'), primary_key=True),
                         db.Column('amenity_id', db.String(36), db.ForeignKey(
                             'amenities.id'), primary_key=True)
                         )


class Place(Base):
    __tablename__ = 'places'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)                                    # foreign key to ref User
    image_url = db.Column(db.String(255), nullable=True)
    owner = db.relationship('User', lazy=True, overlaps="user,places")
    reviews = db.relationship('Review', backref='place', lazy=True)     # foreign key to ref Review

    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(
        self,
        title: str,
        price: float,
        latitude: float,
        longitude: float,
        user_id: str,
        description: str = "",  # Moved to avoid "non-default argument follows default argument"
        image_url: str = None,
        amenities: list = None,
        reviews: list = None
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.image_url = image_url
        self.amenities = amenities if amenities else []
        self.reviews = reviews if reviews else []

    # --- Validations start here ----
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title cannot be empty.")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number.")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        if not value:
            raise ValueError("User ID cannot be empty.")
        return value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Return a dictionary representation of the Place."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
            "image_url": self.image_url,
            # type: ignore
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": []
        }
