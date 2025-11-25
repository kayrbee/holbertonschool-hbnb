from app import db
from .base_class import Base
from sqlalchemy.orm import validates

class Review(Base):
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
#    user = db.Column(db.String(60), nullable=False)
#    place = db.Column(db.String(60), nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)  # foreign key ref'g Place
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # foreign key ref'g User

    def __init__(self, rating: int, text: str, place: str, user: str):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user
        self.place_id = place

    # --- Validations start here ----
    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if not value.strip():
            raise ValueError("Text is a mandatory field")
        return value
    
    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    @validates('user_id')
    def validate_user(self, key, value):
        if not value:
            raise ValueError("User is mandatory")
        if not isinstance(value, str):
            raise TypeError("User must be a string uuid")
        return value
    
    @validates('place_id')
    def validate_place(self, key, value):
        if not value:
            raise ValueError("Place is mandatory")
        if not isinstance(value, str):
            raise TypeError("Place must be a string uuid")
        return value

    def update(self, data):
        """
        The update method should allow updating object attributes based on a dictionary of new values.
        Updates only if value has changed
        """
        for key, value in data.items():
            if key == "rating" and value != self.rating:
                self.rating = value
            if key == "text" and value != self.text:
                self.text = value
        self.save()  # Updates the updated_at timestamp

    def to_dict(self):
        """Returns a dictionary representation of the review."""
        return {
            "id": self.id,
            "rating": self.rating,
            "text": self.text,
            "user": {
                "id": self.user_id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
            "place": self.place_id
        }
