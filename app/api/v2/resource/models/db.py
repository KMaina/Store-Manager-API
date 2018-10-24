"""
File to manage the connection to the database, creation and deletion of tables
"""
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

def generate_admin():
    """Generate the default admin and add to db"""
    gen_admin = """INSERT INTO users (username, password, admin) 
                   VALUES ('admin', 'passadmin', true) 
                   ON CONFLICT (username) DO NOTHING"""
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(gen_admin)
    connection.commit()
