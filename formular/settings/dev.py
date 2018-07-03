from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

API_KEY = '11fa904321b3604060ec25d9fae22f08ff8f11ab'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'formular',
    }
}

SITE_ID = 1