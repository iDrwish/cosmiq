import os
from .base import *

DEBUG = True
# DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        }
#  }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'Cosmiq_cache_table',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': LOCAL_DB_NAME,
        'USER': LOCAL_DB_USER,
        'PASSWORD': LOCAL_DB_PWD
    }
    }
