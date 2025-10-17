from app.models.base_class import Base
# from app.persistence.user_repo import User_Repo
# from app.persistence.place_repo import Place_Repo


class Review(Base):
    def __init__(self, rating: int, comment: str, place_id: str = None, user_id: str = None):
        super().__init__()
        if type(rating) is not int:
            raise TypeError("Rating must be an integer")
        elif 0 < rating <= 6:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 1 and 5")
        if comment != None:
            self.comment = comment
        else:
            raise ValueError("Comment field is mandatory")
        # To do - validate place_id
        if place_id:
            self.place_id = place_id
        else:
            raise ValueError("Place must first exist to be reviewed")
        # To do - validate user_id
        if user_id:
            self.user_id = user_id
        else:
            raise ValueError("User must exist to leave a review")

    def update(self, data):
        """
        The update method should allow updating object attributes based on a dictionary of new values.
        Updates only if value has changed
        """
        for key, value in data.items():
            if key == "rating" and value != self.rating:
                self.rating = value
            if key == "comment" and value != self.comment:
                self.comment = value
        self.save()  # Updates the updated_at timestamp

    # To do:
    # implement delete_review()
    # implement data_validator()
