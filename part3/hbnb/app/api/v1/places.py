from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

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
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Internal server error')
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()

        try:
            data = api.payload or {}

            # normalise amenities to a string
            amenity_value = data.get("amenities")
            if isinstance(amenity_value, list):
                data["amenities"] = ",".join(amenity_value)
            elif amenity_value is None:
                data["amenities"] = ""
            elif not isinstance(amenity_value, str):
                return {"error": "amenities must be a string or a list of strings"}, 400

            place = facade.create_place(data, owner_id=current_user_id)
            d = place.to_dict()

            if "id" not in d and hasattr(place, "id"):
                d["id"] = place.id
            return d, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            print("DEBUG ERROR:", e)
            return {"error": "Internal server error"}, 500

    @api.response(200, 'List of places retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            results = []

            for p in places:
                d = p.to_dict()

                results.append(d)

            return results, 200

        except Exception as e:
            print("DEBUG ERROR:", e)
            return {"error": "Internal server error"}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place_by_id(place_id)
            d = place.to_dict()

            return d, 200
        except LookupError or ValueError as e:
            print("DEBUG ERROR:", e)
            return {"error": "Place or owner not found"}, 404
        except Exception as e:
            print("DEBUG ERROR:", e)
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input or amenity format')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()

        try:
            place = facade.get_place_by_id(place_id)
        except LookupError:
            return {"error": "Place not found"}, 404

        # only owners can update
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Handle missing or invalid JSON
            if not request.data or request.data == b'':
                return {"error": "Request body is empty"}, 400

            # Ensure valid JSON before access api.payload
            if not request.is_json:
                return {"error": "Request must be JSON"}, 400

            # Call api.payload
            data = api.payload or {}

            # Prevent accidental ownership overrides
            if "owner_id" in data and data["owner_id"] != current_user_id:
                 return {"error": "Cannot reassign ownership"}, 403

            # Normalise amenities to a string
            if "amenities" in data:
                raw = data["amenities"]
                if isinstance(raw, list):
                    data["amenities"] = [a.strip() for a in raw if isinstance(a, str) and a.strip()]
                elif isinstance(raw, str):
                    data["amenities"] = [a.strip() for a in raw.split(",") if a.strip()]
                else:
                    return {"error": "amenities must be a string or list of strings"}, 400
            else:
                # Preserve existing amenities if not provided
                data["amenities"] = [a.id for a in place.amenities]

            # Update using facade
            # return model, not _serialize_place
            updated = facade.update_place(place_id, data)
            d = updated.to_dict()

            # attach owner
            owner = facade.get_user_by_id(updated.owner_id)
            d["owner"] = owner.to_dict() if owner else None

            return d, 200

        except LookupError:
            return {"error": "Place not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            print("DEBUG ERROR:", e)
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(401, 'Unauthorized action')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def delete(self, place_id):
        """ Delete a place's information """
        current_user_id = get_jwt_identity()

        try:
            place = facade.get_place_by_id(place_id)
        except LookupError:
            return {"error": "Place not found"}, 404

        # only owners can delete
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_place(place_id)
            return {'success': 'Place deleted successfully'}, 200
        except Exception:
            return {"error": "Internal server error"}, 500
