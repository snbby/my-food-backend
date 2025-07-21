import os
from pathlib import Path

import sentry_sdk

## Envs
MYFOOD_CSV_LINK = os.getenv('MYFOOD_CSV_LINK', '')

# Base
MYFOOD_DEBUG = os.getenv('MYFOOD_DEBUG', 'False').lower() == 'true'
MYFOOD_ENVIRONMENT = os.getenv('MYFOOD_ENVIRONMENT', 'LOCAL')

# Db
MYFOOD_DATABASE_HOST = os.getenv('MYFOOD_DATABASE_HOST', 'localhost')
# MYFOOD_DATABASE_HOST = '172.17.0.1'
MYFOOD_DATABASE_PORT = os.getenv('MYFOOD_DATABASE_PORT', '5432')
MYFOOD_DATABASE_NAME = os.getenv('MYFOOD_DATABASE_NAME', '')
MYFOOD_DATABASE_USER = os.getenv('MYFOOD_DATABASE_USER', '')
MYFOOD_DATABASE_PASS = os.getenv('MYFOOD_DATABASE_PASS', '')
# Sentry
MYFOOD_SENTRY_DSN = os.getenv('MYFOOD_SENTRY_DSN', '')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('MYFOOD_DJANGO_SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = MYFOOD_DEBUG

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

sentry_sdk.init(
    dsn=MYFOOD_SENTRY_DSN,
    environment=MYFOOD_ENVIRONMENT
)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'django.my-food.com', 'django.snobby.es']
CSRF_TRUSTED_ORIGINS = ['https://django.my-food.com', 'https://django.snobby.es']


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myfood',
    'rest_framework',
    'drf_spectacular'
]

# REST_FRAMEWORK = {
    # Below untested
#     # 'DEFAULT_PAGINATION_CLASS': 'myfood.utils.CustomCursorPagination',
#     'PAGE_SIZE': 25
# }

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myfood.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myfood.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': MYFOOD_DATABASE_NAME,
        'USER': MYFOOD_DATABASE_USER,
        'PASSWORD': MYFOOD_DATABASE_PASS,
        'HOST': MYFOOD_DATABASE_HOST,
        'PORT': MYFOOD_DATABASE_PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
MYFOOD_LANGUAGE_CODE = os.getenv('MYFOOD_LANGUAGE_CODE', 'en-EN')
TIME_ZONE = 'Europe/Madrid'
USE_L10N = False
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'admin_static')]

STATIC_URL = '/django-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'django-static/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging
LOGGING = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '{levelname} {asctime} {filename}:{lineno} - {message}',
            'style': '{',
        },
        'access': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '[%d/%b/%Y:%H:%M:%S %z]'
        },
        'sensor_log_format': {
            'format': '%(asctime)s level=%(levelname)s name=%(name)s %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic'
        },    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'myfood': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
}

# Ninja
NINJA_PAGINATION_PER_PAGE = 10