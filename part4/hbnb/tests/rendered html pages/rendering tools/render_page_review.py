#!/usr/bin/python3

from app import create_app
from flask import render_template

app = create_app()

# Create a dummy place object with the fields your template expects
place = {
    "id": "36c9050e-ddd3-4c3b-9731-9f487208bbf2",
    "title": "Sample Place Title"   # You can change this to anything
}

with app.test_request_context():
    html_output = render_template("add_review.html", place=place)
    with open("review_rendered.html", "w", encoding="utf-8") as f:
        f.write(html_output)

print("Rendered HTML written to review_rendered.html")
