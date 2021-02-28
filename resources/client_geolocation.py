from flask_jwt_extended import jwt_required
from flask import request

from external_api import get_location_data
from resources.geolocation import Geolocation


class ClientGeolocation(Geolocation):
    """This class is called with /client_geolocation endpoint."""

    @jwt_required()
    def get(self):
        """Detect client's location based on its IP and save it to the 'geolocations' table."""

        if request.headers.getlist("X-Forwarded-For"):
            self.ip_of_interest = request.headers.getlist("X-Forwarded-For")[0]
        else:
            self.ip_of_interest = request.remote_addr

        try:
            location_info = get_location_data(self.ip_of_interest)
        except Exception as e:
            return self.external_API_error(e)

        self.url_of_interest = None

        return self.save_to_db(location_info)
