"""
File to manage the connection to the database, creation and deletion of tables
"""
import os
import psycopg2
from flask import current_app

def db_connection():
    """Make a connection to the DB"""
    db_path = current_app.config.get('DB_PATH')
    try:
        connection = psycopg2.connect(db_path)
        return connection
    except psycopg2.DatabaseError as e:
        return {'error': '{}'.format(e)}
    
def create_tables():
    """Create all tables"""
    statements = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            admin BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            product_cost INTEGER NOT NULL,
            reorder INTEGER NOT NULL,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sales (
            sales_id SERIAL,
            product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
            totat_cost INT NOT NULL,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            PRIMARY KEY (product_id, sales_id, user_id)
        )
        """)
    connection = db_connection()
    cursor = connection.cursor()
    for statement in statements:
        cursor.execute(statement)
        connection.commit()

def drop_tables():
    """Drops all tables"""
    drops = ["DROP TABLE users CASCADE",
             "DROP TABLE products CASCADE",
             "DROP TABLE sales CASCADE"]

    connection = db_connection()
    cursor = connection.cursor()
    for drop in drops:
        cursor.execute(drop)
        connection.commit()

