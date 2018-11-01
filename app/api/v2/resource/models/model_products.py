"""handles all CRUD operations for the products endpoint"""
import psycopg2
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity

from app.api.v2.resource.models import db

class Products():
    """Class to handle interaction with the products data"""
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
            return {'error':'Fields cannot be empty'}, 401

        # Checks for values less than 1
        if quantity < 1 or product_cost < 1 or reorder < 1:
            return {'error':'Values cannot be less than 1'}, 401

        # Check if a product exists
        product_duplicate = db.check_if_product_exists(name)
        if product_duplicate:
            return product_duplicate

        try:
            new_product = """
                            INSERT INTO 
                            products (product_name, quantity, product_cost, reorder, user_id) 
                            VALUES ('{}','{}','{}','{}','{}')
                            """.format(name, quantity, product_cost, reorder, userid)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(new_product)
            connection.commit()
            response = jsonify({'success':'Product Successfully Created'})
            response.status_code = 201
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem inserting record into the database'})
            response.status_code = 400
            return response

    def delete_product(self, productId):
        """Method to delete a product"""

        # Check if the product exists
        product_id = db.get_db_id(table_name='products', column='product_id', data=productId)
        if product_id == False:
            return {'error':'Product does not exist'}, 404

        try:
            product_delete = "delete from products where product_id = {}".format(productId)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(product_delete)
            connection.commit()
            response = jsonify({'mssuccessg':'Product Successfully Deleted'})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem inserting record into the database'})
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
            return {'error':'Fields cannot be empty'}, 401

        # Checks for values less than 1
        if quantity < 1 or product_cost < 1 or reorder < 1:
            return {'error':'Values cannot be less than 1'}, 401

        # Check if a product exists
        product_duplicate = db.get_quantity_of_products(name)
        if not product_duplicate:
            return {'error':'product does not exist'}, 401

        # Get the quantity added
        get_quantity = db.get_quantity_of_products(name)
        new_total = get_quantity + quantity

        try:
            modify_product = """
                                UPDATE products
                                SET product_name = '{}', 
                                    quantity = '{}', 
                                    product_cost = '{}', 
                                    reorder = '{}', 
                                    user_id='{}' 
                                WHERE product_name = '{}'
                            """.format(name, new_total, product_cost, reorder, userid, name)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(modify_product)
            connection.commit()
            response = jsonify({'success':'Product Successfully Edited'})
            response.status_code = 200
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem inserting record into the database'})
            response.status_code = 400
            return response

    def get_all_products(self):
        """Method to get all products"""
        try:
            all_products = "select product_id, product_name, quantity, product_cost, reorder, username from users inner join products on products.user_id=users.user_id"
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(all_products)
            products = cursor.fetchall()
            products_list = []
            if products is None:
                return {'error':'No products found'}, 404
            if products:
                for product in products:
                    products_dict = {
                        "product_id" : product[0],
                        "product_name" : product[1],
                        "quantity" : product[2],
                        "product_cost" : product[3],
                        "reorder" : product[4],
                        "username" : product[5]
                    }
                    products_list.append(products_dict)
            return {'products' : products_list}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem fetching record from the database'})
            response.status_code = 400
            return response
    
    def get_one_product(self, productId):
        """Method to get all products"""
        try:
            all_products = """select product_id, product_name, quantity, product_cost, reorder, username 
                              from users 
                              inner join products 
                              on products.user_id=users.user_id WHERE product_id={}""".format(productId)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(all_products)
            product = cursor.fetchone()
            if product is None:
                return {'error':'No products found'}, 404
            if product:
                product_dict = {
                    "product_id" : product[0],
                    "product_name" : product[1],
                    "quantity" : product[2],
                    "product_cost" : product[3],
                    "reorder" : product[4],
                    "username" : product[5]
                }
                return {'users' : product_dict}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem fetching record from the database'})
            response.status_code = 400
            return response
