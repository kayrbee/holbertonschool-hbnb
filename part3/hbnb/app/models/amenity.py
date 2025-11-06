from app import db
from .base_class import Base


"""Defines the Amenity model, including validation and serialization logic"""

class Amenity(Base, db.Model):
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    amenities = []
    def __init__(self, name: str):
        """
        Initializes an Amenity instance, validating that the name is a string
        and no longer than 50 characters
        """
        super().__init__()

        # must be a string, less than 50 chars
        if not isinstance (name, str):
            raise TypeError("Amenity name must be a string")
        if len(name) > 50:
            raise ValueError("Amenity length cannot exceed 50 characters")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created at": str(self.created_at),
            "updated at": str(self.updated_at)
        }
        
    # for debugging purpose: when print Amenity object, _repr_ shows useful information instead of a memory address
    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"