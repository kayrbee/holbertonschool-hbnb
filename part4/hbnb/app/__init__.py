
#!/usr/bin/python3
"""
Initialises a Flask app
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, abort, request

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

    # Define the web front-end routes
    @app.route("/login", methods=["GET"])
    def login():
        return render_template("login.html")
    
    @app.route("/")
    def list_places():
        from app.models.place import Place
        places = Place.query.all()
        return render_template("index.html", places=places)

    @app.route("/place")
    def place():
        return render_template("place.html")

    # Note - please fix me!
    @app.route("/add_review", methods=["GET"])
    def add_review():
        # import here to avoid circular imports at module level
        from app.models.place import Place
        place_id = request.args.get("place_id")      
        
        place = Place.query.get(place_id)            
        if not place:
            return {"error": "Place not found"}, 404
        
        return render_template("add_review.html", place=place)

    # Register the API namespaces
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
    api.add_namespace(admin_ns, path='/api/v1/')

    return app
