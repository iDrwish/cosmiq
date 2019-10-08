from .base import *


DEBUG = False
# SECURE_SSL_REDIRECT = True

ADMINS = (
       ('Mohamed Darwish', 'i@cosmiq.io'),)

ALLOWED_HOSTS = ['cosmiq.io', 'www.cosmiq.io', '127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'Cosmiq_cache_table',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROD_DB_NAME,
        'USER': PROD_DB_USER,
        'PASSWORD': PROD_DB_PWD
    }
    }
