from .base import *

print("Using dev settings")

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

# redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://20.40.54.159:8020/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "IGNORE_EXCEPTIONS": True,
        },
        'TIMEOUT': 8040
    }
}

RABBIT_USERNAME = 'karthik'
RABBIT_PASSWORD = 'password'
RABBIT_HOST = '20.40.54.159'
RABBIT_PORT = 8030