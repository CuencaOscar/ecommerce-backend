from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# Local database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Cors headers
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Static and media files
# In development, Django can serve these files directly
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT = BASE_DIR / 'media'
