import os
import sys

print(sys.executable)

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
load_dotenv()


# specify which environement to use in the .env file

# dev, stage, production, local (default) - connection settings for database, redis, rabbitmq are 
# directly specified in the respective settings files for each environment, we can keep them in
# .env.prod, .env.stage, .env.dev, .env.local for more security but for now we are keeping them in direct settings.envirnoment files
    
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
