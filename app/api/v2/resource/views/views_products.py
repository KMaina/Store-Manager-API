"""Views for the Products Resource"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v2.resource.models.model_products import Products

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name',
                    help="You must supply a product name",
                    required='True')
parser.add_argument('quantity',
                    help="You must supply the opening stock amount",
                    required='True', type='int')
parser.add_argument('product_cost',
                    help="You must supply the cost of the product",
                    required='True',
                    type='int')
parser.add_argument('reorder',
                    help="You must supply the reorder amount",
                    required='True',
                    type='int')

class NewProduct(Resource):
    """
    Class to handle creating products
    POST /api/v2/products -> Creates a new products
    """
    @jwt_required
    def post(self):
        """Route to handle creating products"""
        args = parser.parse_args()
        current_user = get_jwt_identity()
        if current_user['admin'] == False:
            return {'msg':'Sorry, this route is only accessible to admins'}, 403
        return Products().add_product(
            args['name'],
            args['quantity'],
            args['product_cost'],
            args['reorder'])
    
    def get(self):
        """Route to get all products"""
        return Products().get_all_products()

class EditProducts(Resource):
    """
    Class to handle editing products
    PUT /api/v2/products/<int:productId> -> Creates a new products
    DELETE /api/v2/products/<int:productId> -> Deletes a product
    """
    @jwt_required
    def delete(self, productId):
        """Route to delete a product"""
        current_user = get_jwt_identity()
        if current_user['admin'] == False:
            return {'msg':'Sorry, this route is only accessible to admins'}, 403
        return Products().delete_product(productId)

    @jwt_required
    def put(self, productId):
        """Route to handle editing a product"""
        args = parser.parse_args()
        current_user = get_jwt_identity()
        if current_user['admin'] == False:
            return {'msg':'Sorry, this route is only accessible to admins'}, 403
        return Products().edit_product(
            args['name'],
            args['quantity'],
            args['product_cost'],
            args['reorder'])

    @jwt_required
    def get(self, productId):
        """Route to handle fetching a single product"""
        return Products().get_one_product(productId)