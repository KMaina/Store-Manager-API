"""Views for the Users Resource"""
from flask_restful import Resource
from flask import request

from app.api.v1.resource.models.model_users import Users

class NewUsers(Resource):
    """
    Class to handle adding and fetching all products
    POST /api/v1/auth/signup -> Creates a new user
    GET /api/v1/users -> Gets all users
    """
    def post(self):
        """Route to handle creating users"""
        return Users().add_user(
            request.json['name'],
            request.json['password'],
            request.json['confirm'])