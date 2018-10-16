"""handles all operations for creating and fetching data relating to products"""

from flask import request, jsonify

# List to hold all products
products = []

def check_if_product_exists(item):
    """
    Helper function to check if a user exists
    Returns True if product already exists, else returns False
    """
    product = [product for product in products if product['name'] == item.rstrip()]
    if product:
        return True
    return False

def check_if_numbers_are_negatives(quantity, price, reorder):
    """
    Helper function to check if any negative numbers were supplied in the JSON object
    Returns True if any number is less than 0, else returns False
    """
    if quantity < 0 or price < 0 or reorder < 0:
        return True
    return False

class Products():
    """Class to handle """
    def add_product(self, name, quantity, price, reorder):
        # Get the JSON object values
        name = request.json.get('name', None)
        quantity = request.json.get('quantity', None)
        price = request.json.get('price', None)
        reorder = request.json.get('reorder', None)

        # Check for duplicate items
        present = check_if_product_exists(name)
        if present:
            return {'msg':'Product already exists'}, 400

        # Checks for numbers less than 0
        size = check_if_numbers_are_negatives(quantity, price, reorder)
        if size:
            return {'msg':'Cannot supply a value less than 0'}, 400
        
        # Add all values to a product dictionary
        product_dict={
            "id": len(products) + 1,
            "name" : name.rstrip(),
            "quantity" : quantity,
            "price" : price,
            "reorder" : reorder
        }
        # Append to the products list
        products.append(product_dict)
        return {"msg": "Product successfully created"}, 201
