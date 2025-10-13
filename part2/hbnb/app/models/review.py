from app.models.base_class import Base


class Review(Base):
    def __init__(self, rating: int, comment: str, place_id: str, user_id: str):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.place_id = place_id
        self.user_id = user_id

    # publish review method
    def publish_review(self):
        self.place_id.add_review()
        # use the place id to look up place and access method in place to append review

    # attach review to user.id

    # To do:
    # - implement validation on place and user - both must exist
    # - rating must be between 1 & 5
    # - comment is mandatory
