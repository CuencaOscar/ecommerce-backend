from .base import *

DEBUG = False

ALLOWED_HOSTS = ['your-production-domain.com']

# Database
# Override base.py settings here for production-specific database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_prod',
        'USER': 'your_production_database_user',
        'PASSWORD': 'your_production_database_password',
        'HOST': 'your_production_database_host',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# Here you might want to set STATIC_ROOT for production and run `collectstatic`
STATIC_ROOT = BASE_DIR / 'staticfiles'
