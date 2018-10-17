"""Initializes the flask app"""

from flask import Flask
from flask_restful import Api

from app.api.v1.resource.views.views_users import NewUsers, GetAllUsers, GetUser

from instance.config import app_config

def create_app(config_name):
    """Factory initialization for the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')   

    # Initialize flask_restful and add routes
    api_endpoint = Api(app)
    api_endpoint.add_resource(NewUsers, '/api/v1/auth/signup')
    api_endpoint.add_resource(GetAllUsers, '/api/v1/users')
    api_endpoint.add_resource(GetUser, '/api/v1/users/<int:user_id>')

    return app
