"""
This module contains class which is called with the /geolocation endpoint.
"""

from flask_jwt_extended import jwt_required
from flask_restx import Resource
from flask import request
import socket

from db import db
from external_api import get_location_data
from models.geolocation import Geolocations


class Geolocation(Resource):
    """This class is called with /geolocation endpoint."""

    @jwt_required()
    def get(self):
        """Detect client's location based on its IP and save it to the 'geolocations' table."""

        if request.headers.getlist("X-Forwarded-For"):
            client_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            client_ip = request.remote_addr

        try:
            location_info = get_location_data(client_ip)
        except Exception as e:
            return self.external_API_error(e)

        return self.save_to_db(location_info)

    @jwt_required()
    def post(self):
        """
        Detect location based on ip or url provided by client as JSON in a body
        and save to the db.
        """

        self.url_of_interest = request.get_json("url").get("url")
        self.ip_of_interest = request.get_json("ip").get("ip")
        if self.url_of_interest and self.ip_of_interest:
            return {
                    "message": "Bad request",
                    "IP data": "To learn IP information, provide either url or ip in the body as JSON, not both!"
                   }, 400
        elif self.url_of_interest:
            self.ip_of_interest = socket.gethostbyname(self.url_of_interest)
        else:
            return {
                    "message": "Bad request",
                    "IP data": "To learn IP information, provide url or ip in the body as JSON."
                   }, 400

        try:
            location_info = get_location_data(self.ip_of_interest)
        except Exception as e:
            return self.external_API_error(e)

        return self.save_to_db(location_info)

    def save_to_db(self, location_info):
        """Instantiate a Geolocation object with location_info as params and save it to db."""

        geolocation_check = Geolocations.find_by_ip_url(self.ip_of_interest, self.url_of_interest)
        if geolocation_check:
            return {
                "message": "IP and URL combination already exists in db.",
                "IP data": geolocation_check.json()
            }, 200

        new_geolocation = Geolocations(
            ip=location_info.get('ip'),
            url=self.url_of_interest,
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
            return {
                "message": "Successfully saved to db",
                "IP data": new_geolocation.json()
            }, 201
        except:
            db.session.rollback()
            return {
                "message": "Something went wrong! Saving to db failed!",
                "IP data": new_geolocation.json()
            }, 500
        finally:
            db.session.close()

    def external_API_error(self, e):
        return {
                   "message": "Sorry, there was a problem with external API. Details: {}".format(e),
                   "IP data": "Null"
                }, 500