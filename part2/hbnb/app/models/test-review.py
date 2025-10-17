#!/usr/bin/python3
# Kat's test script
#   This script exercises the Review class to
#   check the instantiated review object's state
# Can be deleted or incorporated into a proper test after 21/10/25
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

owner = User(first_name="Alice", last_name="Smith",
             email="alice.smith@example.com")
place = Place(title="Cozy Apartment", description="A nice place to stay",
              price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

# # Leave a valid review
# review = Review(1, "Hello", "place_123", "user_123u")
# print("Review: {}\n Rating: {}\n Comment: {}\n Created at: {}\n Updated at: {}".format(
#     review.id, review.rating, review.comment, review.created_at, review.updated_at))

# #  Test for validation of missing fields
# try:
#     review = Review(1, "Hello", place, owner)
#     print("Review saved! Review id: {}".format(review.id))
# except Exception as e:
#     print(e)

#  Test for validation of rating
try:
    review = Review("7", "Hello", place, owner)
    print("Review saved! Review id: {}".format(review.id))
except Exception as e:
    print(e)

# Update review
# print("===============\nUpdate the rating only")
# data = {"rating": 4}
# review.update(data)
# print("Review: {}\n Rating: {}\n Updated at: {}".format(
#     review.id, review.rating, review.updated_at))
# print("===============\nUpdate the comment only")
# data["comment"] = "New comment"
# review.update(data)
# print("Review: {}\n Comment: {}\n Updated at: {}".format(
#     review.id, review.comment, review.updated_at))

# print("===============\nNothing to update")
# review.update()
