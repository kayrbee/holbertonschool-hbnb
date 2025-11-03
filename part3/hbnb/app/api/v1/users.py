from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
# from app.models.user import User
# from app import bcrypt

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

        # password = user_data['password']
        # hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        # user_data['password'] = hashed_pw

        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid Email. Try again'}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

        # new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'message': 'User registered successfully'
        }, 201

    def get(self):
        """ Register all users """
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

    @api.expect(user_model, validate=True)
    @api.response(200, 'Successfully update')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """ Update user info """
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        updated_user = facade.put_user(user_id, data)

        if not updated_user:
            return {'error': 'Update unsuccessful'}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }
