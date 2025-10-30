from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review comment'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user': fields.String(required=True, description='ID of the review author'),
    'place': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Write a new review of a place"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {'id': new_review.id, 'rating': new_review.rating, 'text': new_review.text, 'user': new_review.user, 'place': new_review.place}, 201
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
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError:
            return {"Error": "Review not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500

    @api.expect(review_model)
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload
        try:
            update = facade.update_review(review_id, data)
            return update.to_dict(), 200
        except ValueError as e:
            if str(e) == "Review not found":
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400
        except TypeError:
            return {"error": 'Invalid input data'}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {"success": "Review deleted"}, 200
        except ValueError:
            return {"error": 'Review not found'}, 404
        except Exception:
            return {"error": "Internal server error"}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review for review in reviews], 200
        except ValueError:
            return {"error": "Place not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500
