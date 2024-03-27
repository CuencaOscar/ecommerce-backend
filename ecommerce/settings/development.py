from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# Override base.py settings here for development-specific database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_dev',
        'USER': 'your_development_database_user',
        'PASSWORD': 'your_development_database_password',
        'HOST': 'your_development_database_host',
        'PORT': '5432',
    }
}
