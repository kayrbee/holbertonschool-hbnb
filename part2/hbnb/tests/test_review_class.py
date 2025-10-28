import pytest
from ..app.models.review import Review


def test_review_creation():
    review = Review(rating=2, comment="Comment",
                    user_id="1234", place_id="5678")
    assert review.rating == 2
    assert review.comment == "Comment"
    assert review.user_id == "1234"
    assert review.place_id == "5678"


def test_review_rating_range():
    """Rating < 1"""
    with pytest.raises(ValueError) as exc_info:
        Review(rating=0, comment="Comment",
               user_id="1234", place_id="5678")
    assert str(exc_info.value) == "Rating must be between 1 and 5"
    """Rating > 5"""
    with pytest.raises(ValueError) as exc_info:
        Review(rating=50, comment="Comment",
               user_id="1234", place_id="5678")
    assert str(exc_info.value) == "Rating must be between 1 and 5"


def test_review_rating_is_integer():
    """ Rating=None """
    with pytest.raises(TypeError) as exc_info:
        Review(rating=None, comment="Comment",
               user_id="1234", place_id="5678")
    assert str(exc_info.value) == "Rating must be an integer"

    """ Rating="1" """
    with pytest.raises(TypeError) as exc_info:
        Review(rating="1", comment="Comment",
               user_id="1234", place_id="5678")
    assert str(exc_info.value) == "Rating must be an integer"
