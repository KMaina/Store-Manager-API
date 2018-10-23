"""
File to manage the connection to the database, creation and deletion of tables
"""
import os
import psycopg2

def db_connection(config=None):
    """Make a connection to the DB"""
    if config == 'testing':
        db_name = os.getenv('TEST_DB')
    else:
        db_name = os.getenv('DB_MAIN')
    user = os.getenv('USER')
    password = os.getenv('PASS')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    return  psycopg2.connect(user=user, password=password, host=host, port=port, database=db_name)
    
def create_tables(cursor):
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

    for statement in statements:
        cursor.execute(statement)

def drop_tables(cursor):
    """Drops all tables"""
    drops = ["DROP TABLE users CASCADE",
             "DROP TABLE orders CASCADE",
             "DROP TABLE menus CASCADE",
             "DROP TABLE status CASCADE"]
    for drop in drops:
        cursor.execute(drop)
    cursor.close()
    connection.commit()

def main(config=None):
    """
    This function is run in the command line to automate the connection to the database
    and creation of tables in the database
    """
    connection = db_connection(config=config)
    cursor = connection.cursor()
    create_tables(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()

