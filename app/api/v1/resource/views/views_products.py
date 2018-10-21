"""Views for the Products Resource"""
from flask_restful import Resource, reqparse
from flask import request

from app.api.v1.resource.models.model_products import Products

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', help="You must supply the product name", required='True')
parser.add_argument('quantity', help="You must supply the quantity", required='True')
parser.add_argument('price', help="You must supply the price", required='True')
parser.add_argument('reorder', help="You must supply the reorder amount", required='True')

class NewProducts(Resource):
    """
    Class to handle adding and fetching all products
    POST /api/v1/products -> Creates a new product
    GET /api/v1/products -> Gets all products
    """
    def post(self):
        """Route to handle creating products"""
        args = parser.parse_args()
        return Products().add_product(
            args['name'],
            args['quantity'],
            args['price'],
            args['reorder'])
    
    def get(self):
        """Route to fetch all products"""
        return Products().get_all_products()
    
class GetProduct(Resource):
    """
    Class to handle fetching a specific product
    GET /api/v1/products/<int:product_id> -> Fetches a specific product 
    """
    def get(self, product_id):
        """Route to fetch a specific product"""
        return Products().get_one_product(product_id)

