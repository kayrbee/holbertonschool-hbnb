from app.models.base_class import Base
"""
"""

class Amenity(Base):
    amenities = []
    def __init__(self, name: str):
        """
        Checks input formatting to ensure entries are a string
        and no more than 25 chars, then 
        """
        super().__init__()

        # must be a string, less than 25 chars
        if not isinstance (name, str):
            raise TypeError("Amenity name must be a string")
        if len(name) > 25:
            raise ValueError("Amenity length cannot exceed 25 characters")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }