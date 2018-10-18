"""handles all operations for creating and fetching data relating to sales"""
from flask import request
from flask_jwt_extended import get_jwt_identity

from app.api.v1.resource.models.model_products import products, check_if_product_exists

# List to store all sales
sales = []

def check_for_quantity_of_product(item):
    """
    Checks for the quantity in the db against that ordered
    If the amount order is more than in stock return True, else return False
    """
    product = [product for product in products if product['quantity'] < item]
    if product:
        return True
    return False

class Sales():
    """Class to handle creating and fetching sales"""
    def make_sale(self, product, quantity, price):
        """Method to hande creation of sales"""
        product = request.json.get('product', None)
        quantity = request.json.get('quantity', None)
        price = request.json.get('price', None)

        # Get info regarding the user from the token
        current_user = get_jwt_identity() 

        # Checks if the product exists
        result = check_if_product_exists(product)
        if not result:
            return {'msg':'item does not exist'}, 404
        
        # Checks the amount ordered against that in stock
        amount = check_for_quantity_of_product(quantity)
        if amount:
            return {'msg':'You cannot order more than what is in stock'}, 400
        
        # Finds the total cost for the transaction
        total_cost = price * quantity

        # Add the sale to the sales list
        sales_dict = {
            "id" : len(sales) + 1,
            "name" : product,
            "quantity" : quantity,
            "price" : price,
            "user_id": current_user['id'],
            "total" : total_cost
        }
        sales.append(sales_dict)
        return {'sale': sales_dict}, 201
    