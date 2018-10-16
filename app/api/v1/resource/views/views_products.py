"""Views for the Products Resource"""
from flask_restful import Resource
from flask import request

from app.api.v1.resource.models.model_products import Products

class NewProducts(Resource):
    """
    Class to handle adding and fetching all products
    POST /api/v1/products -> Creates a new product
    GET /api/v1/products -> Gets all products
    """
    def post(self):
        """Route to handle creating products"""
        return Products().add_product(
            request.json['name'],
            request.json['quantity'],
            request.json['price'],
            request.json['reorder'])
    