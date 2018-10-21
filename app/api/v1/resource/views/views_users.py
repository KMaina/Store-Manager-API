"""Views for the Users Resource"""
from flask_restful import Resource, reqparse
from flask import request

from app.api.v1.resource.models.model_users import Users

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', help="You must supply a name", required='True')
parser.add_argument('password', help="You must supply a password", required='True')
parser.add_argument('confirm', help="You must supply a confirmation for your password", required='True')

class NewUsers(Resource):
    """
    Class to handle adding users
    POST /api/v1/auth/signup -> Creates a new user
    """
    def post(self):
        """Route to handle creating users"""
        args = parser.parse_args()
        return Users().add_user(
            args['name'],
            args['password'],
            args['confirm'])

class GetAllUsers(Resource):
    """
    Class to handle fetching all users
    GET /api/v1/users -> Gets all users
    """
    def get(self):
        """Route to fecth all users"""
        return Users().get_all_users()

class GetUser(Resource):
    """
    Class to handle fetching a specific user
    GET /api/v1/users/<int:user_id> -> Fetches a specific user 
    """
    def get(self, user_id):
        return Users().get_one_user(user_id)

class LoginUser(Resource):
    """
    Class to handle user login
    POST '/api/v1/auth/login' -> Logs in a user
    """
    def post(self):
        return Users().login(
            request.json['name'],
            request.json['password'],
        )

