"""Views for the Sales Resource"""
from flask_restful import Resource, reqparse
from flask import request

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', help="You must supply a product name", required='True')
parser.add_argument('quantity', help="You must supply the opening stock amount", required='True', type='int')

class MakeSales(Resource):
    """
    Class to handle creating sales
    POST /api/v2/sales -> Creates a new sale
    """
    @jwt_required
    def post(self):
        """Route to handle creating sales"""
        args = parser.parse_args()
        return Sales().add_sale(
            args['name'],
            args['quantity'])