from flask_jwt_extended import jwt_required
from flask_restx import Resource
from flask import request

from external_api import get_location_data


class ClientGeolocation(Resource):
    """This class is called with /client_geolocation endpoint."""

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