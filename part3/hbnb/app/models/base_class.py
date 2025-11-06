"""
Base class for the common elements of
Place, Amenity, User and Review classes
- uuid
- created_at
- updated_at
"""


from app import db
import uuid
from datetime import datetime
# To do: is the from statement necessary?


class Base(db.Model):
    __abstract__ = True  # Ensures SQLAlchemy does not create a table for BaseModel

    # Creates columns for id, created_at, and updated_at
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
