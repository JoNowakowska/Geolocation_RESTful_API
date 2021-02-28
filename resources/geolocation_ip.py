"""
This module contains class which is called with the /geolocation/<int:ip> endpoint.
"""
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from db import db
from models.geolocation import Geolocations


class GeolocationIP(Resource):
    """This class is called with /geolocation/<string:ip> endpoint."""

    @jwt_required()
    def get(self, ip):
        """Return a record from 'geolocations' table where ip=ip"""

        geo_from_db = Geolocations.find_by_ip(ip)
        if not geo_from_db:
            return {'message': 'Record with ip {} not found in the db.'.format(ip)}, 404

        return {'IP: {}'. format(ip): "{}".format(geo_from_db.json())}, 200

    @jwt_required()
    def delete(self, ip):
        """Delete a record from 'geolocations' table where ip=ip"""

        record = Geolocations.find_by_ip(ip)

        if not record:
            return {"message": "Item with the ip {} not found in the db.".format(ip)}, 404

        try:
            record.delete_from_db()
            db.session.commit()
            return {"message": "Item with the ip {} deleted successfully!.".format(ip)}, 200
        except:
            db.session.rollback()
            return {"message": "Something went wrong! Deleting from the db failed!"}, 500
        finally:
            db.session.close()
