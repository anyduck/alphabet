import os
import yaml


API_TOKEN = os.getenv('API_TOKEN')
WEB_HOST = os.getenv('WEB_HOST')

with open('locales/uk.yml', 'r') as file:
    MESSAGES = yaml.safe_load(file)
