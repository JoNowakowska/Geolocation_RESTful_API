"""
This module contains classes which are called with different routes.
"""

from flask_restx import Resource
from flask import request

from db import db
from external_api import get_location_data
from models.geolocation import Geolocations


class Geolocation(Resource):
    """
    Take care of
    """

    def get(self):
        """
        Detect client's location based on its IP and saves it to database.
        :return:
        """

        if request.headers.getlist("X-Forwarded-For"):
            client_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            client_ip = request.remote_addr

        location_info = get_location_data(client_ip)

        return self.save_to_db(location_info)

    def post(self):
        """
        Detect a location based on IP provided by client in a body as JSON and save it to database.
        :return:
        """

        id_of_interest = request.get_json()['ip_address']  # bulk searches not available in the free plan
        location_info = get_location_data(id_of_interest)

        return self.save_to_db(location_info)

    def save_to_db(self, location_info):
        """
        Instantiate a Geolocation object and save it to db.
        :param location_info: dict
        :return: JSON
        """

        new_geolocation = Geolocations(
            ip=location_info.get('ip'),
            ipv_type=location_info.get('type'),
            continent_code=location_info.get('continent_code'),
            continent_name=location_info.get('continent_name'),
            country_code=location_info.get('country_code'),
            country_name=location_info.get('country_name'),
            region_code=location_info.get('region_code'),
            region_name=location_info.get('region_name'),
            city=location_info.get('city'),
            zip=location_info.get('zip'),
            latitude=location_info.get('latitude'),
            longitude=location_info.get('longitude')
        )

        new_geolocation.add_to_session()

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
