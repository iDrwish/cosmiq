import os
import connection_url
from .base import *


DEBUG = os.environ.get('DEBUG')
if DEBUG == 'TRUE':
    DEBUG = True
else:
    DEBUG = False

# SECURE_SSL_REDIRECT = True

ADMINS = (
       ('Mohamed Darwish', 'i@cosmiq.io'),)

ALLOWED_HOSTS = ['cosmiq.io', 'www.cosmiq.io', 'cosmiq.heroku.com', '*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'Cosmiq_cache_table',
    }
}

if DATABASE_URL:
    DATABASES = {}
    DATABASES['default'] = connection_url.config(DATABASE_URL)
elif PROD_DB_NAME:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROD_DB_NAME,
        'USER': PROD_DB_USER,
        'PASSWORD': PROD_DB_PWD
    }
    }

