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
        """Return json of all of the records saved in the db"""

        all_recs = Geolocations.get_all()
        all_recs_details = [r.json() for r in all_recs]

        return {
            "All records saved to db": all_recs_details
        }

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
        elif self.ip_of_interest:
            pass
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

    @jwt_required()
    def delete(self):
        """Delete a record from 'geolocations' table where ip=ip and url=url"""

        url = request.get_json("url").get("url")
        ip = request.get_json("ip").get("ip")

        if url and ip is None:
            ip = socket.gethostbyname(url)

        record = Geolocations.find_by_ip_url(ip, url)

        if not record:
            return {"message": "Item with the ip={} and url={} not found in the db.".format(ip, url)}, 404

        try:
            record.delete_from_db()
            db.session.commit()
            return {"message": "Item with the ip={} and url={} deleted successfully!.".format(ip, url)}, 200
        except:
            db.session.rollback()
            return {"message": "Something went wrong! Deleting from the db failed!"}, 500
        finally:
            db.session.close()

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
