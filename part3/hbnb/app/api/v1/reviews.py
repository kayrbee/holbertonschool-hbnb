from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review comment'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user': fields.String(required=True, description='ID of the review author'),
    'place': fields.String(required=True, description='ID of the place')
})

# Review model for updating review data, specifically removes required fields
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(),
    'rating': fields.Integer(),
    'place': fields.String(),
    'user': fields.String()
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input, duplicate review, or reviewing own place')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def post(self):
        """Write a new review of a place"""
        current_user_id = get_jwt_identity()

        review_data = api.payload or {}
        try:
            place_id = review_data.get("place")
            if not place_id:
                return {"error": "place_id is required"}, 400

            place = facade.place_repo.get(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            if place.owner_id == current_user_id:
                return {"error": "You cannot review your own place"}, 400

            existing_reviews = facade.get_review_by_user_and_place(
                current_user_id, place_id)
            if existing_reviews:
                return {"error": "You have already reviewed this place."}, 400

            review_data["user"] = current_user_id
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'rating': new_review.rating,
                'text': new_review.text,
                'user': new_review.user_id,
                'place': new_review.place_id
            }, 201

        except (ValueError, TypeError) as e:
            return {"error": f"{e}"}, 400
        except Exception:
            return {"error": "Internal server error"}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.response(500, 'Internal server error')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError:
            return {"Error": "Review not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input or update failure')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)

        # if not admin and doesn't own a review
        if review.user != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            review = facade.review_repo.get(review_id)
            data = api.payload or {}

            if not review:
                return {"error": "Review not found"}, 404

            update = facade.update_review(review_id, data)
            return update.to_dict(), 200

        except ValueError as e:
            if str(e) == "Review not found":
                return {"error": f"{e}"}, 404
            return {"error": f"{e}"}, 400

        except TypeError:
            return {"error": 'Invalid input data'}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Review not found')
    @api.response(500, 'Internal server error')
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()

        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        # Authorisation check
        if not is_admin and review.user != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {"success": "Review deleted"}, 200
        except Exception:
            return {"error": "Internal server error"}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(500, 'Internal server error')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review for review in reviews], 200
        except ValueError:
            return {"error": "Place not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500
