"""Views for the Products Resource"""
from flask_restful import Resource, reqparse
from flask import request

from app.api.v2.resource.models.model_users import Users

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', help="You must supply a product name", required='True')
parser.add_argument('quantity', help="You must supply the opening stock amount", required='True', type='int')
parser.add_argument('product_cost', help="You must supply the cost of the product", required='True', type='int')
parser.add_argument('reorder', help="You must supply the reorder amount", required='True', type='int')

class NewProduct(Resource):
    """
    Class to handle creating products
    POST /api/v2/products -> Creates a new products
    """
    def post(self):
        """Route to handle creating users"""
        args = parser.parse_args()
        return Products().add_product(
            args['name'],
            args['quantity'],
            args['product_cost'],
            args['reorder'])