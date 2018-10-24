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
            print(error)
            response = jsonify({'msg':'Problem fetching record from the database'})
            response.status_code = 400
            return response
            