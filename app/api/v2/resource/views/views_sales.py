"""Views for the Sales Resource"""
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

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

        current_user = get_jwt_identity()
        if current_user['admin'] == True:
            return {'msg':'Sorry, this route is only accessible to sales attendants'}, 403
        return Sales().add_sale(
            args['name'],
            args['quantity'])