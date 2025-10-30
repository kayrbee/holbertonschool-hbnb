from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        try:
            data = api.payload or {}
            if isinstance(data.get("amenities"), str):
                data["amenities"] = [data["amenities"]]

            user_id = get_jwt_identity()
            place = facade.create_place(data, owner_id=user_id)
            d = place.to_dict()
            
            if "id" not in d and hasattr(place, "id"):
                d["id"] = place.id

            owner = facade.get_user_by_id(place.owner_id)
            if owner and hasattr(owner, "to_dict"):
                d["owner"] = owner.to_dict()

            amenities = []
            for amenity_id in d.get("amenities", []):
                a = facade.amenity_repo.get(amenity_id)
                if a and hasattr(a, "to_dict"):
                    amenities.append(a.to_dict())
            d["amenities"] = amenities

            return d, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Internal server error"}, 500


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            results = []
            for p in places:
                d = p.to_dict()

                owner = facade.get_user_by_id(p.owner_id)
                d["owner"] = owner.to_dict() if owner and hasattr(owner, "to_dict") else None

                amenities = []
                for amenity_id in d.get("amenities", []):
                    a = facade.amenity_repo.get(amenity_id)
                    if a and hasattr(a, "to_dict"):
                        amenities.append(a.to_dict())
                d["amenities"] = amenities

                results.append(d)
            return results, 200

        except ValueError:
            return [], 200
        except Exception:
            return {"error": "Internal server error"}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place_by_id(place_id)
            d = place.to_dict()

            owner = facade.get_user_by_id(place.owner_id)
            d["owner"] = owner.to_dict() if owner and hasattr(owner, "to_dict") else None

            amenities = []
            for amenity_id in d.get("amenities", []):
                a = facade.amenity_repo.get(amenity_id)
                if a and hasattr(a, "to_dict"):
                    amenities.append(a.to_dict())
            d["amenities"] = amenities

            return d, 200
        except ValueError:
            return {"error": "Place not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information"""
        try:
            user_id = get_jwt_identity()
            
            place = facade.get_place_by_id(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            
            if place.owner_id != user_id:
                return {"error": "Unauthorized action: You don't own this place"}, 403
            
            payload = api.payload or {}
            if "amenities" in payload and isinstance(payload["amenities"], str):
                payload["amenities"] = [payload["amenities"]]

            # Update using facade
            updated = facade.update_place(place_id, payload)  # return model, not _serialize_place
            d = updated.to_dict()

            owner = facade.get_user_by_id(updated.owner_id)
            d["owner"] = owner.to_dict() if owner and hasattr(owner, "to_dict") else None

            amenities = []
            for amenity_id in d.get("amenities", []):
                a = facade.amenity_repo.get(amenity_id)
                if a and hasattr(a, "to_dict"):
                    amenities.append(a.to_dict())
            d["amenities"] = amenities

            return d, 200

        except LookupError:
            return {"error": "Place not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Internal server error"}, 500
