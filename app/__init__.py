"""Initializes the flask app"""
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# v1 imports
from app.api.v1.resource.views.views_users import NewUsers, GetAllUsers, GetUser, LoginUser
from app.api.v1.resource.views.views_products import NewProducts, GetProduct
from app.api.v1.resource.views.views_sales import MakeSale, GetSpecificSale

# v2 imports
from app.api.v2.resource.models import db

from instance.config import app_config

def create_app(config_name):
    """Factory initialization for the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # create tables in test and main DB
    main()
    main('testing')

    # Catch all 400 errors 
    @app.errorhandler(400)
    def bad_request_error(error):
        """400 error handler."""
        return jsonify({"error": "A bad request was sent to the server."}), 400

    # Catch all 404 errors 
    @app.errorhandler(404)
    def not_found_error(error):
        """404 error handler."""
        return jsonify({"error": "Page not found."}), 404
    
    # Catch all 500 errors 
    @app.errorhandler(500)
    def internal_server_error(error):
        """500 error handler."""
        return jsonify({"error": "Internal server error has occured."}), 500

    # Initialize flask_restful and add routes
    api_endpoint = Api(app)
    
    # Users Resource
    api_endpoint.add_resource(NewUsers, '/api/v1/auth/signup')
    api_endpoint.add_resource(GetAllUsers, '/api/v1/users')
    api_endpoint.add_resource(GetUser, '/api/v1/users/<int:user_id>')
    api_endpoint.add_resource(LoginUser, '/api/v1/auth/login')

    # Products Resource
    api_endpoint.add_resource(NewProducts, '/api/v1/products')
    api_endpoint.add_resource(GetProduct, '/api/v1/products/<int:product_id>')

    # Sales Resource
    api_endpoint.add_resource(MakeSale, '/api/v1/sales')
    api_endpoint.add_resource(GetSpecificSale, '/api/v1/sales/<int:sale_id>')

    # Initializes flask_jwt_extended
    jwt = JWTManager(app)

    return app

