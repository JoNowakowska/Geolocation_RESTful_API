import requests

from db import db
from models.user import User
from tests.base_test import BaseTest, URL
import json


class TestUserRegister(BaseTest):
    def test_post_duplicate_user(self):
        with self.app_context():
            with self.app() as client:
                User(username="TestUsername", password="TestPwd1!").add_to_session()
                db.session.commit()
                response = client.post(f"{URL}/register",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "Username TestUsername already taken. Use another username."}

                self.assertEqual(json.loads(response.data), expected,
                                 "The message returned by the endpoint /register "
                                 "while trying to register an already existing username is not what was expected")
                self.assertEqual(response.status_code, 400,
                                 "The status code returned by the endpoint /register "
                                 "while trying to register an already existing username is not what was expected")

    def test_post_successfully_created(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/register",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "New user 'TestUsername' successfully saved to db"}

                self.assertEqual(json.loads(response.data), expected,
                                 "The message returned by the endpoint /register "
                                 "while registering user successfully is not what was expected")
                self.assertEqual(response.status_code, 201,
                                 "The status code returned by the endpoint /register "
                                 "while registering user successfully is not what was expected")