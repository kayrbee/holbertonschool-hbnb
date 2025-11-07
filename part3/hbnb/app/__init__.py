
#!/usr/bin/python3
"""
Initialises a Flask app
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Instantiates a password encryption class
bcrypt = Bcrypt()

# Instantiates a JWT manager class
jwt = JWTManager()

# Instanstiates a SQLAlchemy class
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register bcrypt with the app instance
    bcrypt.init_app(app)

    app.config.from_object(config_class)

    # Register the jwt middleware with the app instance
    jwt.init_app(app)

    # Register SQLAlchemy  with the app instance
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # move this import block here to avoid circular import
    from app.api.v1.users import api as users_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_ns

    # register the endpoint namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    
    return app
