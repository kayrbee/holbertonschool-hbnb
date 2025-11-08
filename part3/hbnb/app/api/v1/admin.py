from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from functools import wraps
from app.services import facade

api = Namespace('admin', description='Admin-only operations')

# admin role check decorator


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper


# define the USER MODEL for input validation and documentation
admin_user_model = api.model('AdminUser', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password (hashed before saving)'),
    'is_admin': fields.Boolean(required=False, description='Determines user as admin if applied')
})

# USER UPDATE MODEL for updating user data, specifically removes required fields
admin_user_update_model = api.model('AdminUser', {
    'id': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'is_admin': fields.Boolean()
})

# define the AMENITY MODEL for input validation and documentation
admin_amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# REVIEW MODEL for nested value in PLACE MODEL
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review comment'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user': fields.String(required=True, description='ID of the review author'),
    'place': fields.String(required=True, description='ID of the place')
})

# define the PLACE MODEL for input validation and documentation
admin_place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# REVIEW UPDATE MODEL for updating review data, specifically removes required fields
admin_review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(),
    'rating': fields.Integer(),
    'place': fields.String(),
    'user': fields.String()
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @admin_required
    @api.expect(admin_user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Missing required field or email already registered')
    @api.response(403, 'Admin privileges required')
    @api.response(500, 'Internal server error')
    def post(self):
        """ Create new users """
        user_data = api.payload or {}
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'Missing required field: {field}'}, 400

        # Check if email is already in use
        email = user_data.get('email')
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid Email. Try again'}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

        return {
            'id': new_user.id,
            'message': 'User registered successfully'
        }, 201


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @admin_required
    @api.expect(admin_user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Email already in use or Update unsuccessful')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @api.response(500, 'Internal server error')
    def put(self, user_id):
        """ Update user info """
        data = request.json
        email = data.get('email')

        # Check if email is already in use
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # update logic
        try:
            updated_user = facade.put_user(user_id, data)

            if updated_user is None:
                return {'error': 'User not found'}, 404
            if updated_user is False:
                return {'error': 'Update unsuccessful'}, 400

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
            }
        except Exception as e:
            print("SERVER ERROR:", e)
            return {'error': 'Internal server error'}, 500


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @admin_required
    @api.expect(admin_amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Create a new Amenity """
        try:
            data = request.get_json()
            amenity = facade.create_amenity(data)
            return {'id': amenity.id, 'name': amenity.name}, 201
        except Exception:
            return {'error': 'Invalid input data'}, 400


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @admin_required
    @api.expect(admin_amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """ Modify Amenity """
        data = request.get_json()
        name = data.get("name", "").strip()

        if not name:
            return {'error': 'Amenity name cannot be empty'}, 400

        try:
            updated = facade.update_amenity(amenity_id, data)
            return updated, 200
        except ValueError:
            return {'error': 'Amenity not found'}, 404
        except Exception:
            return {'error': 'Invalid input data'}, 400

    @admin_required
    @api.expect(admin_amenity_model)
    @api.response(200, "Amenity deleted")
    @api.response(401, "Unauthorized")
    @api.response(403, "Admin privileges required")
    @api.response(404, "Amenity not found")
    @api.response(500, "Internal server error")
    def delete(self, amenity_id):
        """ Delete an amenity """
        try:
            facade.delete_amenity(amenity_id)
            return {'success': 'Amenity deleted'}, 200
        except ValueError:
            return {'error': 'Amenity not found'}, 404
        except Exception:
            return {'error': 'Internal server error'}, 500


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @admin_required
    @api.expect(admin_place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input or amenity format')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def put(self, place_id):
        """ Bypass ownership restrictions when Modifying Place """
        place = facade.get_place_by_id(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        try:
            payload = api.payload or {}
            if "amenities" in payload and isinstance(payload["amenities"], str):
                payload["amenities"] = [payload["amenities"]]

            # Update using facade
            # return model, not _serialize_place
            updated = facade.update_place(place_id, payload)
            d = updated.to_dict()

            owner = facade.get_user_by_id(updated.owner_id)
            d["owner"] = owner.to_dict() if owner and hasattr(
                owner, "to_dict") else None

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


@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @admin_required
    @api.expect(admin_review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input or update failure')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """ Bypass ownership restrictions when Modifying Review """
        review = facade.review_repo.get(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        data = api.payload or {}
        try:
            update = facade.update_review(review_id, data)
            return update.to_dict(), 200
        except ValueError as e:
            if str(e) == "Review not found":
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400
        except TypeError:
            return {"error": 'Invalid input data'}, 400


@api.route('/reviews/<review_id>')
class AdminReviewDelete(Resource):
    @admin_required
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(500, 'Internal server error')
    def delete(self, review_id):
        """ Bypass ownership restrictions when Deleting Review """
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        try:
            facade.delete_review(review_id)
            return {"success": "Review deleted"}, 200
        except ValueError:
            return {"error": 'Review not found'}, 404
        except Exception:
            return {"error": "Internal server error"}, 500
