from .base import *

print("Using dev settings")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'product_db',
        'USER': 'karthik',
        'PASSWORD': 'password',
        'HOST': '20.40.54.159',
        'PORT': '8016',
    }
}

RABBIT_USERNAME = 'karthik'
RABBIT_PASSWORD = 'password'
RABBIT_HOST = '20.40.54.159'
RABBIT_PORT = 8030