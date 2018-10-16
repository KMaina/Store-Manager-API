"""Unit tests for the product resource"""

import unittest
import json
from app import create_app

class TestProducts(unittest.TestCase):
    """Class containing all tests for the product resource"""
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.product = {
            "name":"Bread",
            "quantity":50,
            "price":50,
            "reorder":20
        }
        self.product_2 = {
            "name":"Soap",
            "quantity":50,
            "price":-1,
            "reorder":20
        }
        self.product_3 = {
            "name":"Toothpaste                 ",
            "quantity":50,
            "price":1,
            "reorder":20
        }     

    def test_add_an_order(self):
        """Tests for adding a new product"""
        response = self.client().post('/api/v1/products', data=json.dumps(self.product), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product successfully created", str(response.data))
    
    def test_if_product_exists(self):
        """Tests if a product already exists"""
        response = self.client().post('/api/v1/products', data=json.dumps(self.product), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Product already exists", str(response.data))
    
    def test_if_arguemnt_has_negative_values(self):
        """Tests if a negative value has been supplied"""
        response = self.client().post('/api/v1/products', data=json.dumps(self.product_2), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot supply a value less than 0", str(response.data))

    def test_if_white_spaces_can_be_supplied(self):
        """Tests if a there are white spaces in the name argument"""
        response = self.client().post('/api/v1/products', data=json.dumps(self.product_3), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product successfully created", str(response.data)) 
        