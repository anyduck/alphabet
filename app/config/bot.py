import os
import yaml


API_TOKEN = os.getenv('API_TOKEN')

with open('locales/uk.yml', 'r') as file:
    MESSAGES = yaml.safe_load(file)
