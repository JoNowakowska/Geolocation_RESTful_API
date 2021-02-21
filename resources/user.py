"""
This module contains classes related to user register and login.

Register class is called with the /register endpoint.
Login class is called with the /login endpoint.
"""
from flask_jwt_extended import create_access_token
from flask_restx import Resource, reqparse
from werkzeug.security import safe_str_cmp

from db import db
from models.user import User

data_parser = reqparse.RequestParser()
data_parser.add_argument("username",
                         required=True,
                         type=str,
                         help="Please provide a username.")
data_parser.add_argument("password",
                         required=True,
                         type=str,
                         help="Please provide a password.")
data_parser.add_argument("admin",
                         required=False,
                         type=int,
                         help="Please provide a privilege level")


class Register(Resource):
    def post(self):
        new_user = data_parser.parse_args()
        username = new_user.get('username')
        if User.find_by_username(username):
            return {"message": "Username {} already taken. Use another username.".format(username)}, 400

        user = User(username=username, password=new_user.get('password'), admin=new_user.get('admin', 0))
        user.add_to_session()

        try:
            db.session.commit()
            return {
                "message": "New user '{}' successfully saved to db".format(new_user.get('username'))
            }, 201
        except:
            db.session.rollback()
            return {
                "message": "Something went wrong! Saving to db failed!"
            }, 500
        finally:
            db.session.close()


class Login(Resource):
    def post(self):
        user = data_parser.parse_args()
        user_login = User.find_by_username(user.get("username"))

        if user_login and safe_str_cmp(user.get("password"), user_login.password):
            access_token = create_access_token(identity=user_login.id, fresh=True)
            print("access_token {}".format(access_token))
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid credentials."}, 401
