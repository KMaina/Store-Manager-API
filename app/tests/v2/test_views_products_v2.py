"""Tests for the Products Resource"""
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
        self.admin = {
            "name":"admin",
            "password":"passadmin"
        }
        self.product1 = {
            "name":"eggs",
            "quantity":30,
            "product_cost":30,
            "reorder":20
        }
        self.product2 = {
            "name":"eggs",
            "quantity":30,
            "reorder":20
        }
        self.product3 = {
            "name":"eggs",
            "quantity":30,
            "product_cost":"",
            "reorder":20
        }
        self.product4 = {
            "name":"eggs",
            "quantity":30,
            "product_cost":-1,
            "reorder":20
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

    def test_add_new_product(self):
        """Test to successfuly add a new product in the database"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
    
    def test_product_already_exists(self):
        """Test to successfuly add a new product in the database"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product1), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Product already exists', str(response.data))
    
    def test_product_missing_values(self):
        """Test to handle missing values"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product2), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must supply the cost of the product', str(response.data))
    
    def test_product_empty_values(self):
        """Test to handle empty values"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product3), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Fields cannot be empty', str(response.data))
    
    def test_product_negative_values(self):
        """Test to handle if values are less than 1"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product4), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Values cannot be less than 1', str(response.data))
    
    def test_delete_a_product(self):
        """Tests to delete a product from the db"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v2/products/1', headers = {"Authorization":"Bearer " + access_token}, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertIn('Product successfully deleted', str(response.data))
    
    def test_delete_a_product_that_doesnt_exist(self):
        """Tests to delete a product that does not exist"""
        response = self.client().post('/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.product1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v2/products/2', headers = {"Authorization":"Bearer " + access_token}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Product does not exist', str(response.data))
