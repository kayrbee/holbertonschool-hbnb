#!/usr/bin/python3
"""
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os  # Used for handling JWT secret key

# Instantiates a password encryption class
bcrypt = Bcrypt()

# Instantiates a JWT manager class
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register bcrypt with the app instance
    bcrypt.init_app(app)

    app.config.from_object(config_class)
    # Register the jwt middleware with the app instance
    jwt.init_app(app)

    # Update the config with the JWT_SECRET_KEY
    app.config.update(
        TESTING=True,
        SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
    )

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # move this import block here to avoid circular import
    from app.api.v1.users import api as users_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns

    # register the endpoint namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
