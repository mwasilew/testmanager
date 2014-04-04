"""
Django settings for testmanager project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mj-b7(j51no0tb5i6bfki9ic2fo*8dkpx2a*=m%(ag$%2xkbnd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testdashboard',
    'testplanner',
    'testrunner'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testmanager.urls'

WSGI_APPLICATION = 'testmanager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)-8s %(message)s',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'testplanner': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/testmanager/testplanner.log',
            'backupCount': 5,
            'when': 'midnight',
            'formatter': 'simple'
        },
        'testrunner': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/testmanager/testrunner.log',
            'backupCount': 5,
            'when': 'midnight',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'testplanner.*': {
            'level': 'WARNING',
            'handlers': ['testplanner'],
            'propagate': False,
        },
        'testrunner.*': {
            'level': 'WARNING',
            'handlers': ['testrunner'],
            'propagate': False,
        },
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
REPOSITORIES_HOME = '/tmp'
# URL used to fetch the job and bundle details using lava_tool
LAVA_SERVER_URL = ''
# regexp used for parsing Jenkins job description in order to get LAVA job ID
LAVA_JOB_ID_REGEXP = ''

try:
    from local_settings import *
except ImportError:
    import random
    import string

    # Create local_settings with random SECRET_KEY.
    char_selection = string.ascii_letters + string.digits
    char_selection_with_punctuation = char_selection + '!@#$%^&*(-_=+)'

    # SECRET_KEY contains anything but whitespace
    secret_key = ''.join(random.sample(char_selection_with_punctuation, 50))
    local_settings_content = "SECRET_KEY = '{0}'\n".format(secret_key)

    with open(os.path.join(PROJECT_ROOT, "local_settings.py"), "w") as f:
        f.write(local_settings_content)

    from local_settings import *

TEMPLATE_DEBUG = DEBUG
