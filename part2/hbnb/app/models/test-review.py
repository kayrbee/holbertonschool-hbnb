#!/usr/bin/python3
# Kat's test script
#   This script exercises the Review class to
#   check the instantiated review object's state
# Can be deleted or incorporated into a proper test after 21/10/25
from app.models.review import Review
review = Review(1, "Hello", "123", "123u")
print(review.rating, review.comment, review.created_at, review.id)
