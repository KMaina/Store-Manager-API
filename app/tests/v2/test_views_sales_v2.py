"""Tests for the Sales Resource"""
import unittest
import json

from app import create_app
from app.api.v2.resource.models import db

class SalesTestCase(unittest.TestCase):
    """Unit testiing for the user regsitration endpoint"""
    def setUp(self):
        """Initialize the app and database connections"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.admin = {"name":"admin", "password":"passadmin"}
        self.reg_user = {"name":"Ken Maina", "password":"mysecret", "confirm":"mysecret"}
        self.login_user = {"name":"Ken Maina", "password":"mysecret"}
        self.product = {"name":"milk", "quantity":30, "product_cost":30, "reorder":20}
        self.sale = {"name":"milk", "quantity":10}
        self.sale1 = {"name":"milk", "quantity":50}
        self.sale2 = {"name":"milk"}
        self.sale3 = {"name":"", "quantity":50}

        with self.app.app_context():
            db.db_connection()
            db.create_tables()
            db.generate_admin()

    def tearDown(self):
        """Drops all tables after tests are done"""
        with self.app.app_context():
            db.db_connection()
            db.drop_tables()

    def test_create_sale_record(self):
        """Test to successfully create a new sale record"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Sale Successfully Created', str(response.data))

    def test_create_sale_as_admin(self):
        """Test to create a new sale record as an admin"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Sorry, this route is only accessible to sales attendants', str(response.data))

    def test_create_sale_record_for_non_existing_product(self):
        """Test to create a sale record for peoducts not in the database"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Product does not exist', str(response.data))

    def test_create_sale_record_if_quantity_is_more_than_in_stock(self):
        """Test to create a sale record if the ordered quantity is larger than that in stock"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale1),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Quantity order is more than that in stock', str(response.data))

    def test_create_sale_record_if_values_are_missing(self):
        """Test to create a sale record if the ordered quantity is larger than that in stock"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale2),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must supply the quantity of the sale', str(response.data))

    def test_create_sale_record_if_inputs_are_empty(self):
        """Test to create a sale record if the inputs are empty"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale3),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Fields cannot be empty', str(response.data))

    def test_to_get_all_sales(self):
        """Test to successfully fetch all sales"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().get('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_to_get_all_sales_as_non_admins(self):
        """Test to fetch all sales as a non admin"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().get('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_to_get_sales_if_non_is_generated(self):
        """Test to fetch sales if no sale has been generated yet"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().get('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_to_get_one_sales(self):
        """Test to successfully fetch a single sale"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.admin),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_admin = json_data.get('access_token')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/api/v2/auth/signup',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.reg_user),
                                      content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        json_data = json.loads(response.data)
        access_token_user = json_data.get('access_token')
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      data=json.dumps(self.product),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product Successfully Created', str(response.data))
        response = self.client().post('api/v2/sales',
                                      headers={"Authorization":"Bearer " + access_token_user},
                                      data=json.dumps(self.sale),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client().get('api/v2/sales/1',
                                      headers={"Authorization":"Bearer " + access_token_admin},
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
