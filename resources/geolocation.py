"""
This module contains class which is called with the /geolocation endpoint.
"""
from flask_jwt_extended import jwt_required
from flask_restx import Resource, reqparse
from flask import request

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

        location_info = get_location_data(client_ip)

        return self.save_to_db(location_info)

    @jwt_required()
    def post(self):
        """Detect location based on IP provided by client as JSON in a body and save to the 'geolocations' table."""

        data_parser = reqparse.RequestParser()
        data_parser.add_argument("ip_address",
                                 required=True,
                                 type=str,
                                 help="Please provide an ip_address.")

        id_of_interest = data_parser.parse_args().get("ip_address")  # bulk searches not available in the free plan

        location_info = get_location_data(id_of_interest)
        print("success! {}".format(id_of_interest))
        return self.save_to_db(location_info)

    def save_to_db(self, location_info):
        """Instantiate a Geolocation object with location_info as params and save it to db."""

        geolocation_check = Geolocations.find_by_ip(location_info.get('ip'))
        if geolocation_check:
            return {
                "message": "IP already exists in db.",
                "IP data": geolocation_check.json()
            }, 200

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
