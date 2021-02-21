"""
This module creates database model for geolocations table.
"""


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
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())

    def json(self):
        """Return self as dictionary."""

        return {
            "id": self.id,
            "ip": self.ip,
            "ipv_type": self.ipv_type,
            "continent_code": self.continent_code,
            "continent_name": self.continent_name,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "region_code": self.region_code,
            "region_name": self.region_name,
            "city": self.city,
            "zip": self.zip,
            "latitude": self.latitude,
            "longitude": self.longitude
            }

    def add_to_session(self):
        """Add self to session."""

        db.session.add(self)

    def delete_from_db(self):
        """Delete the record from db"""

        db.session.delete(self)


    @classmethod
    def find_by_ip(cls, ip):
        """Find a record by its ip and return as dictionary"""

        found_ip = cls.query.filter_by(ip=ip).first()
        return found_ip



