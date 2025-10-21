from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            # Get JSON data from request
            data = api.payload
            if not data:
                return {"error": "No input data provided"}, 400

            # Validate required fields
            required_fields = ["title", "price", "latitude",
                               "longitude", "owner_id", "amenities"]
            missing_fields = [
                field for field in required_fields if field not in data]
            if missing_fields:
                return {
                    "error": "Missing fields: {}".format(", ".join(missing_fields))
                }, 400

            # Normalize amenities (allow string or list)
            amenities = data.get("amenities", [])
            if isinstance(amenities, str):
                amenities = [amenities]
            data["amenities"] = amenities

            # Create and return
            created = facade.create_place(data)
            return created, 201

        except KeyError as e:
            # If a required field is missing in the data
            return {"error": "Missing key: {}".format(str(e))}, 400

        except ValueError as e:
            # If the data is wrong
            return {"error": str(e)}, 400

        except Exception as e:
            # If something else goes wrong
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Get the place from the facade (later connected to your repo)
        place = facade.get_place(place_id)  # expect dict or None
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        existing = facade.get_place_by_id(place_id)
        if not existing:
            return {'error': 'Place not found'}, 404

        data = request.get_json() or {}
        updated = facade.put_place(place_id, data)  # expect dict or None

        if not updated:
            return {'error': 'Update unsuccessful'}, 400

        return updated, 200
