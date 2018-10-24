from flask_restful import Resource, reqparse
from flask import request

from app.api.v2.resource.models.model_users import Users

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', help="You must supply a username", required='True')
parser.add_argument('password', help="You must supply a password", required='True')
parser.add_argument('confirm', help="You must supply a confirmation for your password", required='True')

class LoginUsers(Resource):
    """
    Class to handle adding users
    POST /api/v2/auth/login -> Creates a new user
    """
    def post(self):
        """Route to handle creating users"""
        args = parser.parse_args()
        return Users().login_user(
            args['name'],
            args['password'])

class RegisterUsers(Resource):
    """
    Class to handle adding users
    POST /api/v2/auth/signup -> Creates a new user
    """
    def post(self):
        """Route to handle creating users"""
        args = parser.parse_args()
        return Users().reg_user(
            args['name'],
            args['password'],
            args['confirm'])