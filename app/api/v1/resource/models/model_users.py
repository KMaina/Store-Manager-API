"""handles all operations for creating and fetching data relating to users"""

from flask import request

# List to hold all users
users = []

def check_if_user_exists(item):
    """
    Helper function to check if a user exists
    Returns True if user already exists, else returns False
    """
    user = [user for user in users if user['name'] == item.rstrip()]
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
        if len(users) == 0:
            return {'msg':'No users added yet'}, 404
        return {'users': users}, 200