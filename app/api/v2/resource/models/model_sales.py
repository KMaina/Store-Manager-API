"""handles all CRUD operations for the sales endpoint"""
import psycopg2
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from app.api.v2.resource.models import db

class Sales:
    """Class to handle the CRUD on sales"""
    def add_sale(self, name, quantity):
        """Method to add a sale"""
        name = request.json.get('name', None)
        quantity = request.json.get('quantity', None)

        current_user = get_jwt_identity()

        # Checks for empty fields
        if name == '' or quantity == '':
            return {'msg':'Fields cannot be empty'}, 401

        # Check if a product exists
        product_duplicate = db.check_if_product_exists(name)
        if not product_duplicate:
            return {'msg':'Product does not exist'}, 404

        # Checks for values less than 1
        if quantity < 1:
            return {'msg':'Values cannot be less than 1'}, 401
        
        # Get the quantity added
        get_quantity = db.get_quantity_of_products(name)
        if quantity > get_quantity:
            return {'msg':'Quantity order is more than that in stock'}, 401
        new_quantity = get_quantity - quantity
        
        get_price = db.get_price_of_products(name)
        total_cost = get_price * quantity

        id = db.get_product_id('products', 'product_name', name)

        try:
            modify_product = """UPDATE products 
                                SET quantity = {}
                                WHERE product_name = '{}'""".format(new_quantity, name)
            new_sale = "INSERT INTO \
                          sales (product_id, totat_cost, user_id) \
                          VALUES ('{}','{}',{})".format(id, total_cost, current_user['id'])               
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(modify_product)
            cursor.execute(new_sale)
            connection.commit()
            response = jsonify({'msg':'Sale Successfully Created'})
            response.status_code = 201
            print(response.data)
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'msg':'Problem inserting record into the database'})
            response.status_code = 400
            return response
        

