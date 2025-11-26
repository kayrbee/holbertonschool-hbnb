from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from datetime import timedelta  # to extend token expiry time

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Login route


@api.route('/login', methods=["POST"])
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Success')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """ Authenticate user and return a JWT token """
        credentials = api.payload

        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=3), # extend token exipiry for testing purpose
            additional_claims={"is_admin": user.is_admin}
        )

        return {'access_token': access_token}, 200
