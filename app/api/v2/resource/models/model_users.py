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
                access_token = create_access_token(identity={"username": row[0], "admin": row[2], "id": row[3]})
                response = jsonify({"success":"User Successfully logged in", "access_token":access_token})
                response.status_code = 200
                return response
            response = jsonify({"error" : "Error logging in, credentials not found"})
            response.status_code = 401
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem fetching record from the database'})
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
            return {'error':"Passwords do not match"}, 401

        if len(password) < 6 or len(password) > 12:
            return {'error': "Password length should be between 6 and 12 characters long"}, 401

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
            response = jsonify({'success':'User Successfully Created'})
            response.status_code = 201
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            response = jsonify({'error':'Problem fetching record from the database'})
            response.status_code = 400
            return response

    def get_all_users(self):
        """Method to get all users"""
        try:
            all_users = "SELECT * FROM USERS"
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(all_users)
            users = cursor.fetchall()
            users_list = []
            if users is None:
                return {'error':'No users found'}, 200
            if users:
                for user in users:
                    users_dict = {
                        "user_id" : user[0],
                        "username" : user[1],
                        "admin" : user[3]
                    }
                    users_list.append(users_dict)
            return {'users' : users_list}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'error':'Problem fetching record from the database'})
            response.status_code = 400
            return response

    def get_one_user(self, userId):
        """Method to get one user"""
        try:
            get_user = "SELECT * FROM USERS where user_id = {}".format(userId)
            connection = db.db_connection()
            cursor = connection.cursor()
            cursor.execute(get_user)
            user = cursor.fetchone()
            if user is None:
                return {'error':'User not found'}, 404
            if user:
                users_dict = {
                    "user_id" : user[0],
                    "username" : user[1],
                    "admin" : user[3]
                }
                return {'users' : users_dict}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'error':'Problem fetching record from the database'})
            response.status_code = 400
            return response
