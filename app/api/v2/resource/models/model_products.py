"""handles all CRUD operations for the products endpoint"""
import psycopg2
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from app.api.v2.resource.models import db

class Products():
    def add_product(self, name, quantity, product_cost, reorder):
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