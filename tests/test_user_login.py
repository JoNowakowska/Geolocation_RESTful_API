from db import db
from models.user import User
from tests.base_test import BaseTest, URL
import json


class TestUserLogin(BaseTest):
    def test_post_success(self):
        with self.app_context():
            with self.app() as client:
                User(username="TestUsername", password="TestPwd1!").add_to_session()
                db.session.commit()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                self.assertEqual(response.status_code, 200,
                                 "Improper status code while trying to successfully log in.")
                self.assertIn("access_token", json.loads(response.data).keys(),
                              "Lack of access_token while trying to successfully log in.")

    def test_post_invalid_credentials(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "Invalid credentials."}

                self.assertEqual(response.status_code, 401,
                                 "Improper status code while trying to log in with invalid credentials.")
                self.assertEqual(json.loads(response.data), expected,
                                 "Improper message while trying to log in with invalid credentials.")