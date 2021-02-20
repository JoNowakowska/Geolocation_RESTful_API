"""
This module contains classes which are called with different routes.
"""


from flask_restx import Resource
from flask import request

from external_api import get_location_data


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

    def post(self):
        """
        Detect a location based on IP provided by client in a body as JSON and save it to database.
        :return:
        """

        id_of_interest = request.get_json()['ip_address']  # bulk searches not available in the free plan

        locations_info = get_location_data(id_of_interest)


