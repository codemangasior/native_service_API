import os
from django.utils.crypto import get_random_string


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_string(50)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "api.nativeservice.pl",
    "www.api.nativeservice.pl",
    "192.168.0.106",
    "56b2f4e1.ngrok.io",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Native_Service.apps.NativeServiceConfig",
    "widget_tweaks",
    "crispy_forms",
    "django.contrib.sites",
    "favicon",
]

ROOT_URLCONF = "native_service_API.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "assets/pages")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "native_service_API.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]

ENV_PATH = os.path.abspath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, "public/static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "public/media/")

MEDIA_URL = "/media/"
# Email settings


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SESSION_COOKIE_HTTPONLY = True


""" NativeService lib settings """

LOCAL_HOST_URL = "https://56b2f4e1.ngrok.io/"

# Until production gets the end
HOST_URL = LOCAL_HOST_URL
# HOST_URL = "https://api.nativeservice.pl"

SITE_ID = 1


