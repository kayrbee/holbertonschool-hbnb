from app import db
from .base_class import Base
from sqlalchemy.orm import validates

"""Defines the Amenity model, including validation and serialization logic"""

class Amenity(Base):
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name: str):
        """
        Initializes an Amenity instance, validating that the name is a string
        and no longer than 50 characters
        """
        super().__init__()

    # --- Validations start here ----
    @validates('name')
    def validate_name(self, key, value):
        if not isinstance (value, str):
            raise TypeError("Amenity name must be a string")
        if len(value) > 50:
            raise ValueError("Amenity length cannot exceed 50 characters")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created at": str(self.created_at),
            "updated at": str(self.updated_at)
        }