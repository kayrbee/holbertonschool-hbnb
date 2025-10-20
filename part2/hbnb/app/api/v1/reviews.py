from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Review comment'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the review author'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Write a new review of a place"""
        review_data = api.payload
        required_fields = ['comment', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                return {'Error': f"Missing required field {field}"}, 400
        new_review = facade.create_review(review_data)
        return {'id': new_review.id, 'rating': new_review.rating, 'comment': new_review.comment, 'user_id': new_review.user_id, 'place_id': new_review.place_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews of a place"""
        return "Placeholder GET", 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieve successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        pass

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        pass

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # # Placeholder for the logic to delete a review
        pass


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass
