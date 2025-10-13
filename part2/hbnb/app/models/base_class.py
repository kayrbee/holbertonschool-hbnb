"""
Base class for the common elements of
Place, Amenity, User and Review classes
- uuid
- created_at
- updated_at
"""


import uuid
from datetime import datetime
# To do: is the from statement necessary?


class Base:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Generate random uuid
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
