"""Unit tests for the users resource"""

import unittest
import json
from app import create_app

class TestProducts(unittest.TestCase):
    """Class containing all tests for the users resource"""
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.user = {
            "name":"Ken",
            "password":"pass123",
            "confirm":"pass123"
        }
        self.user1 = {
            "name":"Ken",
            "password":"pass123",
            "confirm":"pass124"
        }
        self.user2 = {
            "name":"Ken",
            "password":"pass",
            "confirm":"pass"
        }

        def test_add_user(self):
            """Tests for adding a new user"""
            response = self.client().post('/api/v1/auth/signup', data=json.dumps(self.user), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn("User Successfully created", str(response.data))
        
        def test_add_user_wrong_passwords(self):
            """Tests for checking if password match"""
            response = self.client().post('/api/v1/auth/signup', data=json.dumps(self.user1), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Passwords do not match", str(response.data))
        
        def test_password_length(self):
            """Tests for the length of the passwords"""
            response = self.client().post('/api/v1/auth/signup', data=json.dumps(self.user2), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Password length should be between 6 and 12 characters long", str(response.data))

        def test_fetch_all_users(self):
            """Tests for fetching all users"""
            response = self.client().get('/api/v1/users')
            self.assertEqual(response.status_code, 200)
        