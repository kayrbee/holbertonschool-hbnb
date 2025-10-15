#!/usr/bin/python3

from flask import Flask
from flask_restx import Api
from api.v1.amenities import api as amenity_ns
from api.v1.places import api as places_ns
from api.v1.reviews import api as reviews_ns
from api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)

    api = Api(
        app, 
        version='1.0',
        title='HBNB API',
        description='API for managing amenities, places,' \
              'reviews, and users'
    )

    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
