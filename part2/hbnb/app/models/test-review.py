#!/usr/bin/python3
from app.models.review import Review
# This returns "ModuleNotFoundError: No module named 'app'"
# Review = __import__('review').Review  # This works
# from .review import Review
# from part2.hbnb.app.models.review import Review
# part2/hbnb/app/models/review.py
# Testing
review = Review(1, "Hello", "123", "123u")
print(review.rating, review.comment, review.created_at, review.id)
