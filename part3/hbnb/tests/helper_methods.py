from flask_jwt_extended import create_access_token
from app import db
import uuid

""" These helper methods are used in the test suites to set up required states """


def create_test_user(is_admin=False):
    from app.models import User
    unique_email = f"john.doe_{uuid.uuid4().hex}@example.com"
    user = User(
        first_name="Mary",
        last_name="Contrary",
        email=unique_email,
        password="password",
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    return user


def login(user):
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"is_admin": user.is_admin}
    )

    return access_token


def create_amenity(amenity_name):
    from app.models import Amenity
    amenity = Amenity(amenity_name)
    db.session.add(amenity)
    db.session.commit()

    return amenity


def create_place(user_id):
    from app.models import Place
    amenity = create_amenity("Pool")
    # amenity_id = amenity.id
    place = Place(
        title="Beach House",
        description="A nice place to stay",
        price=200,
        latitude=-37.8,
        longitude=144.9,
        owner_id=user_id,
        amenities=[amenity]
    )
    db.session.add(place)
    db.session.commit()

    return place


def create_review(place_id, reviewer_id):
    from app.models import Review
    review = Review(
        text="Highly recommend",
        rating=5,
        place=place_id,
        user=reviewer_id
    )

    db.session.add(review)
    db.session.commit()

    return review
