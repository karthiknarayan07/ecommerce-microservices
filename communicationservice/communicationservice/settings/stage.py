from .base import *

print("Using stage settings")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'communication_db',
        'USER': 'karthik',
        'PASSWORD': 'password',
        'HOST': '20.40.54.159',
        'PORT': '8018',
    }
}

RABBIT_USERNAME = 'karthik'
RABBIT_PASSWORD = 'password'
RABBIT_HOST = '20.40.54.159'
RABBIT_PORT = 8030