"""Unit tests for the sales resource"""

import unittest
import json
from app import create_app

from app.api.v1.resource.models.model_users import generate_admin

class TestSales(unittest.TestCase):
    """Class to handle tests for the sales resource"""
    def setUp(self):
        """Sets up for the actual tests"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.admin = {
            "name":"admin",
            "password":"admin123"
        }
        self.user_reg1 = {
            "name":"John",
            "password":"pass123",
            "confirm":"pass123"
        }
        self.user_login1 = {
            "name":"John",
            "password":"pass123"
        }
        self.user_reg2 = {
            "name":"Mike",
            "password":"pass123",
            "confirm":"pass123"
        }
        self.user_login2 = {
            "name":"Mike",
            "password":"pass123"
        }
        self.user_reg3 = {
            "name":"Dave",
            "password":"pass123",
            "confirm":"pass123"
        }
        self.user_login3 = {
            "name":"Dave",
            "password":"pass123"
        }
        self.sale = {
            "product":"Soap",
            "quantity":4,
            "price":30
        }
        self.product = {
            "name" : "Soap",
            "quantity" : 4,
            "price" : 30,
            "reorder":20
        }
        self.product2 = {
            "name" : "Eggs",
            "quantity" : 4,
            "price" : 30,
            "reorder":20
        }
    
    def test_add_sale_record(self):
        """Test to add a record as an attendant"""
        response = self.client().post('/api/v1/auth/signup', data=json.dumps(self.user_reg2), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res_login = self.client().post('/api/v1/auth/login', data=json.dumps(self.user_login2), content_type='application/json')
        json_output = json.loads(res_login.data)
        access_token = json_output.get('msg')
        self.assertEqual(res_login.status_code, 200)
        res_product = self.client().post('/api/v1/products', data=json.dumps(self.product), content_type='application/json')
        self.assertEqual(res_product.status_code, 201)
        resp_sale = self.client().post('/api/v1/sales', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.sale), content_type='application/json')
        self.assertEqual(resp_sale.status_code, 201)
    
    def test_add_sale_record_as_admin(self):
        """Test to add a sale record if user is admin"""
        generate_admin()
        res_login = self.client().post('/api/v1/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_output = json.loads(res_login.data)
        access_token = json_output.get('msg')
        self.assertEqual(res_login.status_code, 200)
        res_product = self.client().post('/api/v1/products', data=json.dumps(self.product2), content_type='application/json')
        self.assertEqual(res_product.status_code, 201)
        resp_sale = self.client().post('/api/v1/sales', headers = {"Authorization":"Bearer " + access_token}, data=json.dumps(self.sale), content_type='application/json')
        self.assertEqual(resp_sale.status_code, 403)
        self.assertIn('Sorry, this route is not accessible to admins', str(resp_sale.data))

    def test_get_sale_if_user_is_admin(self):
        """Tests if an admin can fetch all sales"""
        generate_admin()
        res_login = self.client().post('/api/v1/auth/login', data=json.dumps(self.admin), content_type='application/json')
        json_output = json.loads(res_login.data)
        access_token = json_output.get('msg')
        self.assertEqual(res_login.status_code, 200)
        response = self.client().get('/api/v1/sales', headers = {"Authorization":"Bearer " + access_token})
        self.assertEqual(response.status_code, 200)

    def test_get_sale_if_user_is_not_admin(self):
        """Tests if a non-admin can fetch all sales"""
        response = self.client().post('/api/v1/auth/signup', data=json.dumps(self.user_reg1), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res_login = self.client().post('/api/v1/auth/login', data=json.dumps(self.user_login1), content_type='application/json')
        json_output = json.loads(res_login.data)
        access_token = json_output.get('msg')
        self.assertEqual(res_login.status_code, 200)
        response = self.client().get('/api/v1/sales', headers = {"Authorization":"Bearer " + access_token})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Sorry, this route is only accessible to admins", str(response.data

