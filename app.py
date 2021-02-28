"""
This is the main module of the app. It contains the app instance (app).
"""

import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from db import db
from resources.client_geolocation import ClientGeolocation
from resources.geolocation import Geolocation
from resources.geolocation_ip import GeolocationIP
from resources.user import Register, Login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

api = Api(app)
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Geolocation, '/geolocation')
api.add_resource(ClientGeolocation, '/client_geolocation')
api.add_resource(GeolocationIP, '/geolocation/<string:ip>')

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True)