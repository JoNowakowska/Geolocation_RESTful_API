"""
This is the main module of the app. It contains the app instance (app).
"""

import os

from flask import Flask
from flask_restx import Api

from db import db
from resources.geolocation import Geolocation


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

api = Api(app)
api.add_resource(Geolocation, '/geolocation')


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True)