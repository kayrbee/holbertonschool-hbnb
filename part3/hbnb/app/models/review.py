from app.models.base_class import Base


class Review(Base):
    def __init__(self, rating: int, text: str, place: str, user: str):
        super().__init__()
        self.rating = rating
        self.text = text
        self.place = place
        self.user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user: str):
        if not user:
            raise ValueError("User is mandatory")
        if not isinstance(user, str):
            raise TypeError("User must be a string uuid")
        self._user = user

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place: str):
        if not place:
            raise ValueError("Place is mandatory")
        if not isinstance(place, str):
            raise TypeError("Place must be a string uuid")
        self._place = place

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating: int):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = rating

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        if not text:
            raise ValueError("Text is a mandatory field")
        self._text = text

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
            "user": self.user,
            "place": self.place
        }
