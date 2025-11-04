from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import request
from app.services import facade
from app.models.user import User
from app import bcrypt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password (hashed before saving)')
})

# User model for updating user data, specifically removes required fields
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'is_admin': fields.Boolean()
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Missing required field or email already registered')
    @api.response(403, 'Admin privileges required')
    @api.response(500, 'Internal server error')
    def post(self):
        """Register a new user"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload or {}
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'Missing required field: {field}'}, 400

        # check if email is already in use
        if facade.get_user_by_email(user_data['email']):
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
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input or email already in use')
    @api.response(403, 'Unauthorized action or admin privileges required')
    @api.response(404, 'User not found')
    @api.response(500, 'Internal server error')
    def put(self, user_id):
        """ Update user info """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        is_admin = claims.get("is_admin", False)
        is_self = str(user_id) == str(current_user_id)
        
        if not is_admin and not is_self:
            return {'error': 'Unauthorized action'}, 403
        
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        email = data.get('email')

        # prevent users changing email or pw
        if not claims.get("is_admin", False):
            if "email" in data or "password" in data:
                return {"error": "You cannot modify email or password"}, 400

        # ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.put_user(user_id, data)

            if not updated_user:
                return {'error': 'Update unsuccessful'}, 400

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }

        except Exception as e:
            print("SERVER ERROR:", e)
            return {"error": "Internal server error"}, 500
