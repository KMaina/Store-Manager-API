"""Views for the Users Resource"""
from flask_restful import Resource
from flask import request

from app.api.v1.resource.models.model_users import Users

class NewUsers(Resource):
    """
    Class to handle adding users
    POST /api/v1/auth/signup -> Creates a new user
    """
    def post(self):
        """Route to handle creating users"""
        return Users().add_user(
            request.json['name'],
            request.json['password'],
            request.json['confirm'])

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