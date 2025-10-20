from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify
from flask import request

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            data = request.get_json()
            amenity = facade.create_amenity(data)
            return {"id": amenity.id, "name": amenity.name}, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [a.to_dict() for a in amenities], 200
        except ValueError as e:
            return{"error": str(e)}, 404

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        return facade.get_amenity(amenity_id)
    
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            data = request.get_json()
            updated = facade.update_amenity(amenity_id, data)
            return updated, 200
        except ValueError as e:
            return {"error": "Amenity not found"}, 404
        except Exception as e:
            return {"error": "Invalid input data"}, 400
        