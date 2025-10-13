from app.models.base_class import Base
"""
"""

class Amenity(Base):
    amenities = []
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description
