import pytest
from app.models.review import Review


def test_review_creation():
    review = Review(rating=2, text="Comment",
                    user="1234", place="5678")
    assert review.rating == 2
    assert review.text == "Comment"
    assert review.user == "1234"
    assert review.place == "5678"


def test_review_rating_range():
    """Rating < 1"""
    with pytest.raises(ValueError) as exc_info:
        Review(rating=0, text="Comment",
               user="1234", place="5678")
    assert str(exc_info.value) == "Rating must be between 1 and 5"
    """Rating > 5"""
    with pytest.raises(ValueError) as exc_info:
        Review(rating=50, text="Comment",
               user="1234", place="5678")
    assert str(exc_info.value) == "Rating must be between 1 and 5"


def test_review_rating_is_integer():
    """ Rating=None """
    with pytest.raises(TypeError) as exc_info:
        Review(rating=None, text="Comment",
               user="1234", place="5678")
    assert str(exc_info.value) == "Rating must be an integer"

    """ Rating="1" """
    with pytest.raises(TypeError) as exc_info:
        Review(rating="1", text="Comment",
               user="1234", place="5678")
    assert str(exc_info.value) == "Rating must be an integer"
