import os
import sys

print(sys.executable)

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
load_dotenv()

environment = os.getenv("DJANGO_SETTINGS_ENVIRONMENT")
if environment == "development":
    print('running gunicorn in development')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communicationservice.settings.dev')
elif environment == "stage":
    print('running gunicorn in stage')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communicationservice.settings.stage')
elif environment == "production":
    print('running gunicorn in production')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communicationservice.settings.prod')
else:
    print('running gunicorn in local')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communicationservice.settings.local')


application = get_wsgi_application()
