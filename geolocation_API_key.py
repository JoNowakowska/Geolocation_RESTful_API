"""
This file accesses a Geolocation API Access Key from the os environment variables.

To obtain your access key, you can go to 'https://ipstack.com/signup/free' and get yours for free.
Then, create the os environment variable naming it as 'GEOLOCATION_API_KEY'.
"""


import os

API_KEY = os.environ.get('GEOLOCATION_API_KEY')

