from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

API_KEY = 'e006cf1902b132d33727d4d438c6a97990aab478'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'formular',
    }
}

SITE_ID = 1