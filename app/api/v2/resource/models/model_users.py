"""handles all operations for creating and fetching data relating to users"""
import psycopg2
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from flask import current_app
from app.api.v2.resource.models import db

class Users():
    """Class to handle users"""
    def login_user(self, name, password):
        """Logs in a user"""
        name = request.json.get('name', None)
        password = request.json.get('password', None)
        
        # Check for empty inputs
        if name == '' or password == '':
            return {'error': 'Fields cannot be empty'}, 401

        try:
            get_user = "SELECT username, password, admin, user_id \
                        FROM users \
                        WHERE username = '" + name + "' AND password = '" + password + "'"
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(get_user)
            row = cursor.fetchone()
            if row is not None:                
                access_token = create_access_token(identity={"username": row[0] , "admin": row[2], "id": row[3]})
                response = jsonify({"msg":"User Successfully logged in", "access_token":access_token})
                response.status_code = 200
                return response
            response = jsonify({"msg" : "Error logging in, credentials not found"})
            response.status_code = 401
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'msg':'Problem fetching record from the database'})
            response.status_code = 400
            return response
    
    def reg_user(self, name, password, confirm):
        """Method to handle user creation"""
        name = request.json.get('name', None)
        password = request.json.get('password', None)
        confirm = request.json.get('confirm', None)

        # Check for empty inputs
        if name == '' or password == '' or confirm == '':
            return {'error': 'Fields cannot be empty'}, 401
        
        if password != confirm:
            return {'msg':"Passwords do not match"}, 401

        if len(password) < 6 or len(password) > 12:
            return {'msg': "Password length should be between 6 and 12 characters long"}, 401

        duplicate = db.check_if_user_exists(name)
        if duplicate:
            return duplicate

        try:
            add_user = "INSERT INTO \
                        users (username, password, admin) \
                        VALUES ('" + name +"', '" + password +"',  false )"
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(add_user)
            connection.commit()
            response = jsonify({'msg':'User Successfully Created'})
            response.status_code = 201
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'msg':'Problem fetching record from the database'})
            response.status_code = 400
            return response
