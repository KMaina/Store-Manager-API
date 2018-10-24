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
            db.main_test()
            
    
    def test_user_login(self):
        """Successfully log into the app"""
        response = self.client().post('/api/v2/auth/signup', data=json.dumps({
            "name":"admin",
            "password":"passadmin"
        }), content_type='application/json')
        connection = db.db_connection_test()
        cursor = connection.cursor()

        self.assertEqual(response.status_code, 200)
        self.assertIn('User Successfully Logged In', str(response.data))

    def test_no_user_in_db(self):
        """Test if the user is not in the database"""
        response = self.client().post('/api/v2/auth/signup', data=json.dumps({
            "name":"ken",
            "password":"mypass"
        }), content_type='application/json')
        connection = db.db_connection_test()
        cursor = connection.cursor()

        self.assertEqual(response.status_code, 401)
        self.assertIn('Sorry, credentials not found', str(response.data)) 
    
    def test_empty_credentials(self):
        """Test for empty values"""
        response = self.client().post('/api/v2/auth/signup', data=json.dumps({
            "name":"",
            "password":"mypass"
        }), content_type='application/json')
        connection = db.db_connection_test()
        cursor = connection.cursor()

        self.assertEqual(response.status_code, 401)
        self.assertIn('Fields cannot be empty', str(response.data))
    
    def test_missing_credentials(self):
        """Test for missing parameters"""
        response = self.client().post('/api/v2/auth/signup', data=json.dumps({
            "password":"mypass"
        }), content_type='application/json')
        connection = db.db_connection_test()
        cursor = connection.cursor()

        self.assertEqual(response.status_code, 401)
        self.assertIn('You must supply a username', str(response.data)) 