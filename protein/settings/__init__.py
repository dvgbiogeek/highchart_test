"""
Django settings for protein project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '0mfc+)wqv7sjb2f@)&m!1w^s(8r7zg7@9)7)=5u#x^o81s#*kb'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'protein',
    'composition',
    'functional_tests',
    'glossary',
    'account',
    'resources',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'protein.urls'

WSGI_APPLICATION = 'protein.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'protein',
        'USER': 'danielleglick',
        'PASSWORD': 'aw3edr5',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '../static/'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static/'))

STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'), 'static',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s: %(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file1': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose'
        },
        'file2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'protein.log',
            'formatter': 'verbose'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address': ('frozen-stream-5430.papertrailapp.com', 11111)
        }
    },
    'loggers': {
        'django': {
            'handlers': ['syslog'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'composition': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
        },
        'glossary': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
        },
        'account': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
        }
    }
}

TASTYPIE_DEFAULT_FORMATS = ['json']

TASTYPIE_FULL_DEBUG = True

LOGIN_URL = '/login/'

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '../static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

try:
    from protein.settings.local_settings import *
except ImportError:
    pass
