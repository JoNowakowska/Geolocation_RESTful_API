"""
This module creates database model for geolocation.
"""


from datetime import datetime

from db import db


class Geolocations(db.Model):
    __tablename__ = 'geolocations'

    id = db.Column(db.Integer(), primary_key=True)
    ip = db.Column(db.String(), unique=True, nullable=False)
    ipv_type = db.Column(db.String(10))
    continent_code = db.Column(db.String(10))
    continent_name = db.Column(db.String(60))
    country_code = db.Column(db.String(10))
    country_name = db.Column(db.String(150))
    region_code = db.Column(db.String(50))
    region_name = db.Column(db.String(150))
    city = db.Column(db.String(150))
    zip = db.Column(db.String(50))
    latitude = db.Column(db.Numeric())
    longitude = db.Column(db.Numeric())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def add_to_session(self):
        """
        Add self to session.
        :return: None
        """

        db.session.add(self)

    @classmethod
    def find_by_ip(cls, ip):
        """
        Find record by its ip.
        :param ip: str
        :return:
        """
        print(cls.query.filter_by(ip=ip).first())