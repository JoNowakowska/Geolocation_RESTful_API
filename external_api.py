"""
This module contains a function that connects to the external geolocation API to detect the location.

The location is detected based on IP or URL pasted to the request body as JSON.
"""


import requests

from geolocation_API_key import API_KEY


GEO_API_URL = "http://api.ipstack.com/"  # https is only for paid subscription plan


def get_location_data(ip):
    """
    Connect to the external API and return a json response with location based on ip.
    """

    full_url = "{}/{}?access_key={}".format(GEO_API_URL, ip, API_KEY)
    response = requests.get(full_url)
    location_data = response.json()

    return location_data

