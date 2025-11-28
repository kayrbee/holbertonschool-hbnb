#!/usr/bin/python3

from app import create_app
from flask import render_template

app = create_app()

with app.test_request_context():
    html_output = render_template("place.html")
    with open("place_rendered.html", "w", encoding="utf-8") as f:
        f.write(html_output)

print("Rendered HTML written to place_rendered.html")
