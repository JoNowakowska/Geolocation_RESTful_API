"""
This module creates database model for geolocations table.
"""


from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)
    admin = db.Column(db.Integer(), default=0)

    def add_to_session(self):
        """Add self to the session"""

        return db.session.add(self)

    @classmethod
    def find_by_username(cls, username):
        """Find a record by username and return it"""

        return cls.query.filter_by(username=username).first()