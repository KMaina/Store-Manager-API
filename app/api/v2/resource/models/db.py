"""File to manage the connection to the database, creation and deletion of tables"""
import psycopg2
from flask import current_app

def db_connection():
    """Make a connection to the DB"""
    db_path = current_app.config.get('DATABASE_URL')
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

def generate_admin():
    """Generate the default admin and add to db"""
    gen_admin = """
                INSERT INTO
                users (username, password, admin)
                VALUES ('admin', 'passadmin', true)
                ON CONFLICT (username) DO NOTHING
                """
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(gen_admin)
    connection.commit()

def check_if_user_exists(name):
    """
    Helper function to check if a user exists
    Returns a message if a user already exists
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}'".format(name))
        connection.commit()
        username = cursor.fetchone()
        cursor.close()
        connection.close()
        if username:
            return {'error' : 'User already exists'}, 401
    except (Exception, psycopg2.DatabaseError) as error:
        return {'error' : '{}'.format(error)}, 401

def check_if_product_exists(name):
    """
    Helper function to check if a product exists
    Returns a message if a product already exists
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE product_name = '{}'".format(name))
        connection.commit()
        product = cursor.fetchone()
        cursor.close()
        connection.close()
        if product:
            return {'error' : 'Product already exists'}, 401
    except (Exception, psycopg2.DatabaseError) as error:
        return {'error' : '{}'.format(error)}, 400

def get_db_id(table_name=None, column=None, data=None):
    """
    Helper function to fetch an id from the db
    Returns the id of a product if it exists
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {} WHERE {} = {}".format(table_name, column, data))
        connection.commit()
        get_id = cursor.fetchone()
        cursor.close()
        connection.close()
        if get_id == None:
            return False
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return {'error' : '{}'.format(error)}, 400

def get_quantity_of_products(product):
    """
    Helper function to get the quantity of a product
    Returns the quantity of the product
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT quantity FROM products WHERE product_name = '{}'".format(product))
        connection.commit()
        product = cursor.fetchone()
        cursor.close()
        connection.close()
        if product:
            return product[0]
    except (Exception, psycopg2.DatabaseError) as error:
        return {'error' : '{}'.format(error)}, 400

def get_price_of_products(product):
    """
    Helper function to get the price of a product
    Returns the price of the product
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT product_cost FROM products WHERE product_name = '{}'".format(product))
        connection.commit()
        price = cursor.fetchone()
        cursor.close()
        connection.close()
        if price:
            return price[0]
    except (Exception, psycopg2.DatabaseError) as error:
        return {'error' : '{}'.format(error)}, 400

def get_product_id(table_name=None, column=None, data=None):
    """
    Helper function to fetch an id from the db
    Returns the id of a product if it exists
    """
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table_name, column, data))
        connection.commit()
        get_id = cursor.fetchone()
        cursor.close()
        connection.close()
        if get_id:
            return get_id[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {'error' : '{}'.format(error)}, 400
