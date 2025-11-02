from flask_restx import Namespace, Resource, fields
from app.services import facade
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
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Write a new review of a place"""
        review_data = api.payload or {}
        user_id = get_jwt_identity() 
        try:
            # must include place field
            place_id = review_data.get("place")
            if not place_id:
                return {"error": "place_id is required"}, 400
            
            place = facade.place_repo.get(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            if place.owner_id == user_id:
                return {"error": "You cannot review your own place"}, 400
            
            existing_reviews = facade.get_review_by_user_and_place(user_id, place_id)
            if existing_reviews:
                return {"error": "You have already reviewed this place."}, 400
            
            review_data["user"] = user_id
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'rating': new_review.rating,
                'text': new_review.text,
                'user': new_review.user,
                'place': new_review.place
            }, 201
            
        except (ValueError, TypeError) as e:
            return {"error": f"{e}"}, 400
        except Exception:
            print("SERVER ERROR:", type(e), e)
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
        
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_jwt_identity()
        try:
            review = facade.review_repo.get(review_id)
        
            if not review:
                return {"error": "Review not found"}, 404

            # only review owner can modify
            if review.user != user_id:
                return {"error": "Unauthorised action"}, 403
            
            update = facade.update_review(review_id, data)
            return update.to_dict(), 200
        
        except ValueError as e:
            if str(e) == "Review not found":
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400
        
        except TypeError:
            return {"error": 'Invalid input data'}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        try:
            review = facade.review_repo.get(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            
            # only review owner can delete
            if review.user != user_id:
                return {"error": "Unauthorised action"}, 403
            
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
