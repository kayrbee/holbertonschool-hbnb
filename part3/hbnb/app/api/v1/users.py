from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app.models.user import User
from app import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password (hashed before saving)')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user"""
        user_data = api.payload or {}
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'Missing required field: {field}'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid Email. Try again'}, 400
        except Exception as e:
            return {f'{e}'}, 500

        return {
            'id': new_user.id,
            'message': 'User registered successfully'
        }, 201

    def get(self):
        """ Get all users """
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200


@api.route('/<user_id>', methods=['GET', 'PUT'])
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user_by_id(user_id)

        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name, 'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'Successfully update')
    @api.response(400, 'Invalid input data')
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    def put(self, user_id):
        """ Update user info (cannot modify email or password)"""
        auth_user_id = get_jwt_identity()
        
        # only logged-in user can update their details
        if str(user_id) != str(auth_user_id):
            return {"error": "Unauthorized action"}, 403
        
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json() or {}
        
        # prevent changing email or pw
        if "email" in data or "password" in data:
            return {"error": "You cannot modify email or password"}, 400
        
        try:
            updated_user = facade.put_user(user_id, data)

            if not updated_user:
                return {'error': 'Update unsuccessful'}, 400

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
            
        except Exception as e:
            print("SERVER ERROR:", e)
            return {"error": "Internal server error"}, 500
