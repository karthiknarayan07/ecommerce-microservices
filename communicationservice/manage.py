#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv
load_dotenv()

def main():
    
    
    # specify which environement to use in the .env file
    
    # dev, stage, production, local (default) - connection settings for database, redis, rabbitmq are 
    # directly specified in the respective settings files for each environment, we can keep them in
    # .env.prod, .env.stage, .env.dev, .env.local for more security but for now we are keeping them in direct settings.envirnoment files
    
    
    environment = os.getenv("DJANGO_SETTINGS_ENVIRONMENT")
    
    if environment == "development":
        print("Loading development settings file for Django configurations")
        os.environ["DJANGO_SETTINGS_MODULE"] = "communicationservice.settings.dev"
    elif environment == "stage":
        print("Loading stage settings file for Django configurations")
        os.environ["DJANGO_SETTINGS_MODULE"] = "communicationservice.settings.stage"
    elif environment == "production":
        print("Loading production settings file for Django configurations")
        os.environ["DJANGO_SETTINGS_MODULE"] = "communicationservice.settings.prod"
    else:
        print("Loading local settings file for Django configurations")
        os.environ["DJANGO_SETTINGS_MODULE"] = "communicationservice.settings.local"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
