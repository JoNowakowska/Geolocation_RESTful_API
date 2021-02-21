"""
This module contains class which is called with the /geolocation/<int:ip> endpoint.
"""

from flask_restx import Resource
from flask import request

from db import db
from external_api import get_location_data
from models.geolocation import Geolocations


class GeolocationIP(Resource):
    """This class is called with /geolocation/<string:ip> endpoint."""

    def get(self, ip):
        """Return a record from 'geolocations' table where ip=ip"""

        geo_from_db = Geolocations.find_by_ip(ip)
        return {
            'IP: {}'. format(ip): "{}".format(geo_from_db)
        }
