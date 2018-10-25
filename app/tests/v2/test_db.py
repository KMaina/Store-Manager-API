"""Tests the database and tables creation"""
import unittest

from app import create_app
from app.api.v2.resource.models import db

class DBCase(unittest.TestCase):
    """Unit testiing for the user regsitration endpoint"""
    def setUp(self):
        """Initialize the app and database connections"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            db.db_connection()
            db.create_tables()

    def tearDown(self):
        """Drops all tables after tests are done"""
        with self.app.app_context():
            db.db_connection()
            db.drop_tables()
