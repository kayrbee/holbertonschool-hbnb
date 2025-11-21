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
})


@api.route('/')
class UserList(Resource):
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
        """ Update user info - except email and password"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        is_self = str(user_id) == str(current_user_id)
        is_admin = claims.get("is_admin", False)
        if not (is_self or is_admin):
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload or {}
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
                'email': updated_user.email,
            }, 200

        except Exception as e:
            print("SERVER ERROR:", e)
            return {"error": "Internal server error"}, 500
