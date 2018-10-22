"""Runs the flask app after intializing it"""

import os

from app import create_app

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

posrt = os.environ.get("PORT", 5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
