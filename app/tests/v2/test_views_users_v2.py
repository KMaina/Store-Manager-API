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
