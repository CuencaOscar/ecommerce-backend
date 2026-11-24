"""Settings for the test suite and CI: in-memory SQLite, no external services."""

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = ["testserver"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
