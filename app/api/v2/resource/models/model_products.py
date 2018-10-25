"""handles all CRUD operations for the products endpoint"""
import psycopg2
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from app.api.v2.resource.models import db

class Products():
    def add_product(self, name, quantity, product_cost, reorder):
        """Method to add a product"""
        name = request.json.get('name', None)
        quantity = request.json.get('quantity', None)
        product_cost = request.json.get('product_cost', None)
        reorder = request.json.get('reorder', None)
        
        # Get the ID of the user who created the product
        current_user = get_jwt_identity()
        userid = current_user['id']

        # Checks for empty fields
        if name == '' or quantity == '' or product_cost == '' or reorder == '':
            return {'msg':'Fields cannot be empty'}, 401
        
        # Checks for values less than 1
        if quantity < 1 or product_cost < 1 or reorder < 1:
            return {'msg':'Values cannot be less than 1'}, 401
        
        # Check if a product exists
        product_duplicate = db.check_if_product_exists(name)
        if product_duplicate:
            return product_duplicate

        try:
            new_product = "INSERT INTO \
                          products (product_name, quantity, product_cost, reorder, user_id) \
                          VALUES ('{}','{}','{}','{}','{}')".format(name, quantity, product_cost, reorder, userid)
            
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(new_product)
            connection.commit()
            response = jsonify({'msg':'Product Successfully Created'})
            response.status_code = 201
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'msg':'Problem inserting record into the database'})
            response.status_code = 400
            return response
    
    def delete_product(self, productId):
        """Method to delete a product"""

        # Check if the product exists
        id = db.get_db_id(table_name = 'products', column = 'product_id', data = productId)
        if id == False:
            return {'msg':'Product does not exist'}, 404
        
        try:
            product_delete = "delete from products where product_id = {}".format(productId)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(product_delete)
            connection.commit()
            response = jsonify({'msg':'Product Successfully Deleted'})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'msg':'Problem inserting record into the database'})
            response.status_code = 400
            return response
 
    def edit_product(self, name, quantity, product_cost, reorder):
        """Method to edit a product"""
        name = request.json.get('name', None)
        quantity = request.json.get('quantity', None)
        product_cost = request.json.get('product_cost', None)
        reorder = request.json.get('reorder', None)

        # Get the ID of the user who created the product
        current_user = get_jwt_identity()
        userid = current_user['id']

        # Checks for empty fields
        if name == '' or quantity == '' or product_cost == '' or reorder == '':
            return {'msg':'Fields cannot be empty'}, 401
        
        # Checks for values less than 1
        if quantity < 1 or product_cost < 1 or reorder < 1:
            return {'msg':'Values cannot be less than 1'}, 401
        
        # Check if a product exists
        product_duplicate = db.get_quantity_of_products(name)
        if not product_duplicate:
            return {'msg':'product does not exist'}, 401
        
        # Get the quantity added
        get_quantity = db.get_quantity_of_products(name)
        new_total = get_quantity + quantity
        
        try:
            modify_product = """UPDATE products 
                                SET product_name = '{}', 
                                    quantity = '{}', 
                                    product_cost = '{}', 
                                    reorder = '{}', 
                                    user_id='{}' 
                                WHERE product_name = '{}'""".format(name, new_total, product_cost, reorder, userid, name)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(modify_product)
            connection.commit()
            response = jsonify({'msg':'Product Successfully Edited'})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'msg':'Problem inserting record into the database'})
            response.status_code = 400
            return response
