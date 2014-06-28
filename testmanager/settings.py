# Copyright (C) 2014 Linaro Limited
#
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>
#
# This file is part of Testmanager.
#
# Testmanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation
#
# Testmanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Testmanager.  If not, see <http://www.gnu.org/licenses/>.

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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
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

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login"
LOGOUT_URL = "/logout"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'
REPOSITORIES_HOME = '/tmp'
# URL used to fetch the job and bundle details using lava_tool (including LAVA username)
# example: https://username@lava.server/RPC2/
LAVA_SERVER_URL = ''
# regexp used for parsing Jenkins job description in order to get LAVA job ID
LAVA_JOB_ID_REGEXP = ''
# list of LAVA status names meaning the jobs is running
LAVA_JOB_RUNNING_STATUSES = ['']
# list of status names that mean Jenkins build is running
# RUNNING is artificial as Jenkins doesn't provide such status 
# it is introduced in testmanager import scripts
JENKINS_BUILD_RUNNING_STATUSES = ['RUNNING', 'ERROR']

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
