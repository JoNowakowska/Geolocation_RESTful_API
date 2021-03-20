import json

from db import db
from models.user import User
from models.geolocation import Geolocations
from tests.base_test import BaseTest, URL


class TestRecipeResource(BaseTest):
    def setUp(self):
        super(TestRecipeResource, self).setUp()
        with self.app_context(), self.app() as client:
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

    def test_get_all_from_db_success_empty(self):
        with self.app_context(), self.app() as client:
            response = client.get(f"{URL}/geolocation",
                                  headers={"Authorization": f"Bearer {self.access_token}"}
                                  )

        expected = {"All records saved to db": []}

        self.assertDictEqual(json.loads(response.data), expected,
                             "Message returned when showing all records from empty db is incorrect.")
        self.assertEqual(response.status_code, 200,
                         "Status code returned when showing all records from empty db is incorrect.")

    def test_get_all_from_db_success_not_empty(self):
        with self.app_context(), self.app() as client:
            new_geo = Geolocations(ip="127.0.0.1")
            new_geo.add_to_session()
            db.session.commit()
            response = client.get(f"{URL}/geolocation",
                                  headers={"Authorization": f"Bearer {self.access_token}"}
                                  )

            expected = {"All records saved to db": [
                {
                    "id": 1,
                    "ip": "127.0.0.1",
                    "url": None,
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
            ]
            }

            self.maxDiff = None

            self.assertDictEqual(json.loads(response.data), expected,
                                 "Message returned when when showing all records from not empty db is incorrect.")
            self.assertEqual(response.status_code, 200,
                             "Status code returned when showing all records from not empty db is incorrect.")

    def test_post_location_by_ip_success(self):
        with self.app_context(), self.app() as client:
            response = client.post(f"{URL}/geolocation",
                                   headers={
                                       "Content-Type": "application/json",
                                       "Authorization": f"Bearer {self.access_token}"},
                                   data=json.dumps({"ip": "134.201.250.155"})
                                   )

            expected = {"message": "Successfully saved to db",
                        "IP data": {
                            "id": 1,
                            "ip": "134.201.250.155",
                            "url": None,
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

    def test_post_location_by_url_success(self):
        with self.app_context(), self.app() as client:
            response = client.post(f"{URL}/geolocation",
                                   headers={
                                       "Content-Type": "application/json",
                                       "Authorization": f"Bearer {self.access_token}"},
                                   data=json.dumps({"url": "google.com"})
                                   )

            expected = {"message": "Successfully saved to db",
                        "IP data": {
                            "id": 1,
                            "ip": "142.250.185.174",
                            "url": "google.com",
                            "ipv_type": "ipv4",
                            "continent_code": "NA",
                            "continent_name": "North America",
                            "country_code": "US",
                            "country_name": "United States",
                            "region_code": "CA",
                            "region_name": "California",
                            "city": "Mountain View",
                            "zip": "94043",
                            "latitude": "37.4191589355469",
                            "longitude": "-122.075408935547"
                        }
                        }

            self.maxDiff = None

            self.assertDictEqual(json.loads(response.data), expected,
                                 "Message returned after successfully saving url of interest is incorrect.")
            self.assertEqual(response.status_code, 201,
                             "Status code returned after successfully saving url of interest is incorrect.")

    def test_post_location_by_ip_url_fail(self):
        with self.app_context(), self.app() as client:
            response = client.post(f"{URL}/geolocation",
                                   headers={
                                       "Content-Type": "application/json",
                                       "Authorization": f"Bearer {self.access_token}"},
                                   data=json.dumps({"ip": "134.201.250.155",
                                                    "url": "google.com"})
                                   )

            expected = {
                "message": "Bad request",
                "IP data": "To learn IP information, provide either url or ip in the body as JSON, not both!"
            }

            self.assertDictEqual(json.loads(response.data), expected,
                                 "Message returned after request failed due to providing both id and url incorrect.")
            self.assertEqual(response.status_code, 400,
                             "Status code returned after request failed due to providing both id and url incorrect.")

    def test_delete_success(self):
        with self.app_context(), self.app() as client:
            new_geo = Geolocations(id=1,
                                   ip="134.201.250.155",
                                   url=None,
                                   ipv_type="ipv4",
                                   continent_code="NA",
                                   continent_name="North America",
                                   country_code="US",
                                   country_name="United States",
                                   region_code="CA",
                                   region_name="California",
                                   city="Los Angeles",
                                   zip="90012",
                                   latitude="34.0655517578125",
                                   longitude="-118.240539550781"
                                   )
            new_geo.add_to_session()
            db.session.commit()

            response = client.delete(f"{URL}/geolocation",
                                     headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.access_token}"},
                                     data=json.dumps({"ip": "134.201.250.155"})
                                     )

            expected = {"message": "Item with the ip=134.201.250.155 and url=None deleted successfully!."}

            self.assertDictEqual(json.loads(response.data), expected,
                                 "Message returned after request successfully deleted a record by its id incorrect.")
            self.assertEqual(response.status_code, 200,
                             "Status code returned after request successfully deleted a record by its id incorrect.")

    def test_delete_not_exists(self):
        with self.app_context(), self.app() as client:
            response = client.delete(f"{URL}/geolocation",
                                     headers={
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.access_token}"},
                                     data=json.dumps({"ip": "134.201.250.155"})
                                     )

            expected = {"message": "Item with the ip=134.201.250.155 and url=None not found in the db."}

            self.assertDictEqual(json.loads(response.data), expected,
                                 "Message returned after request failed to delete a non-existing record from db by ip incorrect.")
            self.assertEqual(response.status_code, 404,
                             "Status code returned after request failed to delete a non-existing record from db by ip incorrect.")
