import json

from db import db
from models.user import User
from models.geolocation import Geolocations
from tests.base_test import BaseTest, URL


class TestRecipeResource(BaseTest):
    def setUp(self):
        super(TestRecipeResource, self).setUp()
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
                self.access_token = json.loads(response.data)['access_token']

    def test_get_location_success(self):
        with self.app_context():
            with self.app() as client:
                response = client.get(f"{URL}/geolocation",
                                      headers={"Authorization": f"Bearer {self.access_token}"}
                                      )

        expected = {"message": "Successfully saved to db",
                    "IP data": {
                        "id": 1,
                        "ip": "127.0.0.1",
                        "ipv_type": None,
                        "continent_code": None,
                        "continent_name": None,
                        "country_code": None,
                        "country_name": None,
                        "region_code": None,
                        "region_name": None,
                        "city": None,
                        "zip": None,
                        "latitude": None,
                        "longitude": None
                        }
                    }

        self.maxDiff = None

        self.assertDictEqual(json.loads(response.data), expected,
                             "Message returned after successfully saving client's ip is incorrect.")
        self.assertEqual(response.status_code, 201,
                         "Status code returned after successfully saving client's ip is incorrect.")

    def test_get_location_already_exists(self):
        with self.app_context():
            with self.app() as client:
                new_geo = Geolocations(ip="127.0.0.1")
                new_geo.add_to_session()
                db.session.commit()
                response = client.get(f"{URL}/geolocation",
                                      headers={"Authorization": f"Bearer {self.access_token}"}
                                      )

                expected = {"message": "IP already exists in db.",
                            "IP data": {
                                "id": 1,
                                "ip": "127.0.0.1",
                                "ipv_type": None,
                                "continent_code": None,
                                "continent_name": None,
                                "country_code": None,
                                "country_name": None,
                                "region_code": None,
                                "region_name": None,
                                "city": None,
                                "zip": None,
                                "latitude": None,
                                "longitude": None
                            }
                            }

                self.maxDiff = None

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned after trying to save not unique client's ip is incorrect.")
                self.assertEqual(response.status_code, 200,
                                 "Status code returned after trying to save not unique client's ip is incorrect.")

    def test_post_location_success(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/geolocation",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {self.access_token}"},
                                      data=json.dumps({"ip_address": "134.201.250.155"})
                                      )

                expected = {"message": "Successfully saved to db",
                            "IP data": {
                                "id": 1,
                                "ip": "134.201.250.155",
                                "ipv_type": "ipv4",
                                "continent_code": "NA",
                                "continent_name": "North America",
                                "country_code": "US",
                                "country_name": "United States",
                                "region_code": "CA",
                                "region_name": "California",
                                "city": "Los Angeles",
                                "zip": "90012",
                                "latitude": "34.0655517578125",
                                "longitude": "-118.240539550781"
                                }
                            }

                self.maxDiff = None

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned after successfully saving ip of interest is incorrect.")
                self.assertEqual(response.status_code, 201,
                                 "Status code returned after successfully saving ip of interest is incorrect.")