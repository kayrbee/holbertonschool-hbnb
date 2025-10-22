from app.models.base_class import Base


class Review(Base):
    def __init__(self, rating: int, text: str, place: str, user: str):
        super().__init__()
        if type(rating) is not int:
            raise TypeError("Rating must be an integer")
        elif 0 < rating <= 6:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 1 and 5")
        if text != None:
            self.text = text
        else:
            raise ValueError("Text field is mandatory")
        if place:
            self.place = place
        else:
            raise ValueError("Place is mandatory")
        if user:
            self.user = user
        else:
            raise ValueError("User is mandatory")

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
        """Return a dictionary representation of the review."""
        return {
            "id": self.id,
            "rating": self.rating,
            "text": self.text,
            "user": self.user,
            "place": self.place
        }
