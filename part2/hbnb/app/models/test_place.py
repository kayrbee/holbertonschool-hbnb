import pytest
from models.place import Place

def test_place_creation():
    """Test that a Place object is created correctly"""
    place = Place(
        title="Beach House",
        description="A nice place to stay",
        price=200,
        latitude=-37.8,
        longitude=144.9,
        owner_id="user123",
        amenities=["wifi", "pool"]
    )

    assert place.title == "Beach House"
    assert place.description == "A nice place to stay"
    assert place.price == 200
    assert place.latitude == -37.8
    assert place.longitude == 144.9
    assert place.owner_id == "user123"
    assert "wifi" in place.amenities
    assert "pool" in place.amenities
    print("Place creation test passed!")
