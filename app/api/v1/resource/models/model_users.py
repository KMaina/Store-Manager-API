"""handles all operations for creating and fetching data relating to users"""

from flask import request
from flask_jwt_extended import create_access_token

# List to hold all users
users = []

def generate_admin():
    users_dict = {
        "id": 0,
        "name" : "admin",
        "password" : "admin123",
        "admin" : True
    }
    users.append(users_dict)

def check_if_user_exists(item):
    """
    Helper function to check if a user exists
    Returns True if user already exists, else returns False
    """
    user = [user for user in users if user['name'] == item.rstrip()]
    if user:
        return True
    return False

def verify_credentials(name, password):
    """
    Helper function to check if passwords match
    Returns True if user already exists, else returns False
    """
    user = [user for user in users if user['name'] == name and user['password'] == password]
    if user:
        return True
    return False

class Users():
    """Class to handle users"""
    def add_user(self, name, password, confirm):
        name = request.json.get('name', None)
        password = request.json.get('password', None)
        confirm = request.json.get('confirm', None)
    
        if password != confirm:
            return {'msg':"Passwords do not match"}, 400

        if len(password) < 6 or len(password) > 12:
            return {'msg': "Password length should be between 6 and 12 characters long"}, 400

        duplicate = check_if_user_exists(name)
        if duplicate:
            return {'msg':'User already exists'}, 400    
        
        user_dict = {
            "id": len(users) + 1,
            "name" : name.rstrip(),
            "password" : password,
            "admin" : False
        }
        users.append(user_dict)
        return {'msg':"User Successfully created"}, 201
    
    def get_all_users(self):
        "Fetch all users"
        if len(users) == 0:
            return {'msg':'No users added yet'}, 404
        return {'users': users}, 200
    
    def get_one_user(self, user_id):
        """Fetches a specific user from the users list"""
        user = [user for user in users if user['id'] == user_id]
        if user:
            return {'user': user[0]}, 200
        return {'msg':'User not found'}, 404

    def login(self, name, password):
        name = request.json.get('name', None)
        password = request.json.get('password', None)
        
        credentials = verify_credentials(name, password)
        if not credentials:
            return {'msg':'Error logging in, ensure username or password are correct'}, 400
        
        user = [user for user in users if user['name'] == name.rstrip()]
        access_token = create_access_token(identity={'name':user[0]['name'], 'id':user[0]['id'], 'admin':user[0]['admin']})
        return {'msg':access_token}

