"""
This module contains class which is called with the /geolocation endpoint.
"""

from flask_jwt_extended import jwt_required
from flask_restx import Resource
from flask import request

from db import db
from external_api import get_location_data
from models.geolocation import Geolocations


def create_add_to_session(location_info):
    """
    Check if IP already exists in db,
    if not then instantiate a Geolocation object with location_info as params and add it to session.
    """

    geolocation_check = Geolocations.find_by_ip(location_info.get('ip'))
    if geolocation_check:
        return {
            "message": "IP already exists in db.",
            "IP data": geolocation_check.json()
        }

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

    return {
               "message": "Success!",
               "IP data": new_geolocation.json()
           }


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

    # to be removed after a new post is created (below that one):
    @jwt_required()
    def post(self):
        """Detect location based on IP provided by client as JSON in a body and save to the 'geolocations' table."""

        id_of_interest = request.get_json("ip_address").get("ip_address")  # bulk searches not available in the free plan
        location_info = get_location_data(id_of_interest)

        return self.save_to_db(location_info)

    @jwt_required()
    def post(self):
        """
        Detect location(s) based on list of IPs and/or list of URLs provided by client as JSON in a body
        and save to the 'geolocations' table.
        """

        ip_of_interest_list = request.get_json("IP").get("IP")
        if len(ip_of_interest_list) > 0:
            ips_message = self.check_return_geo_by_ip(ip_of_interest_list)

        urls_message = ""

        final_message = {
            "Geolocations by IP": ips_message,
            "Geolocations by URL": urls_message
        }

        return self.save_to_db(final_message)

    def check_return_geo_by_ip(self, ip_of_interest_list):
        """
        Check geolocation information at ipstack.com using the ip_of_interest_list (one ip at a time),
        instantiate new Geolocations objects and add them to a session,
        return geo information as 2 lists of dicts:
        - ip_success list with geo info of items saved to db
        - ip_already_exist with geo info of items that were not saved to db as would be duplicates.
        """

        ip_success = []
        ip_already_exist = []
        for ip in ip_of_interest_list:
            location_info = get_location_data(ip)
            result = create_add_to_session(location_info)
            message = result.get("message")
            geo_data = result.get("IP data")
            if message == "Success!":
                ip_success.append(geo_data)
            elif message == "IP already exists in db.":
                ip_already_exist.append(geo_data)
        final_message = {
            "IPs successfully saved to db": ip_success,
            "IPs already existed in db": ip_already_exist
        }

        return final_message

    def save_to_db(self, final_message):
        """Save to db all of the objects added to the session."""

        try:
            db.session.commit()
            return {
                "message": "Process finished successfully!",
                "IP data": final_message
            }, 201
        except:
            db.session.rollback()
            return {
                "message": "Something went wrong! Saving to db failed!",
                "IP data": final_message
            }, 500
        finally:
            db.session.close()
