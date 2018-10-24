import unittest
import json

from app import create_app
from app.api.v2.resource.models import db

class UserTestCase(unittest.TestCase):
    """Unit testiing for the user regsitration endpoint"""
    def setUp(self):
        """Initialize the app and database connections"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            "name" : "Ken Maina",
            "password" : "mysecret",
            "confirm" : "mysecret"
        }
        self.user2 = {
            "name" : "John Smith",
            "confirm" : "mysecret"
        }
        self.user3 = {
            "name" : "John Smith",
            "password" : "",
            "confirm" : "mysecret"
        }
        self.user4 = {
            "name" : "John Smith",
            "password" : "pass",
            "confirm" : "pass"
        }
    
        with self.app.app_context():
            db.db_connection()
            db.create_tables()
            db.generate_admin()
        
    def tearDown(self):
        """Drops all tables after tests are done"""
        with self.app.app_context():
            db.db_connection()
            db.drop_tables()
    
    def test_user_login(self):
        """Successfully log into the app"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('User Successfully logged in', str(response.data))

    def test_no_user_in_db(self):
        """Test if the user is not in the database"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"ken",
            "password":"mypass"
        }), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('Error logging in, credentials not found', str(response.data)) 
    
    def test_empty_credentials(self):
        """Test for empty values"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"",
            "password":"mypass"
        }), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('Fields cannot be empty', str(response.data))
    
    def test_missing_credentials(self):
        """Test for missing parameters"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "password":"mypass"
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('You must supply a username', str(response.data))

    def test_user_register(self):
        """Test to successfuly register a new user"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User Successfully Created', str(response.data))
    
    def test_register_with_empty_inputs(self):
        """Test to create a user with empty inputs"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user2), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must supply a password', str(response.data))
    
    def test_register_user_as_non_admin(self):
        """Test to register a new user as a non admin"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user), content_type='application/json')
        response = self.client().post('/api/v2/auth/login', data=json.dumps({"name":"Ken Maina","password":"mysecret"}), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Sorry, only admins are allowed to access this route', str(response.data))
    
    def test_user_register_empty_fields(self):
        """Test to register a new user with empty inputs"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user3), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Fields cannot be empty', str(response.data))
    
    def test_user_register_illegal_passwords(self):
        """Test to register a new user with illegal inputs"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user4), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Password length should be between 6 and 12 characters long', str(response.data))
    
    def test_user_register_twice(self):
        """Test to register an existing user"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/v2/auth/signup', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('User already exists', str(response.data))