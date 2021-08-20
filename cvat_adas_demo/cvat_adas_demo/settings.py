"""
Django settings for cvat_adas_demo project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
# import sys
# import fcntl
# import shutil
# import subprocess
# import mimetypes
from distutils.util import strtobool
from pathlib import Path

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INTERNAL_IPS = ['127.0.0.1']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tcl0yht0@*z-r*v)$c&vkm$68+&s3m6cvw6*qhw&2^^y3d+nn)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cvat_adas_demo.engine',
    'cvat_adas_demo.authentication',
    'cvat_adas_demo.dataset_manager',
    'cvat_adas_demo.dataset_repo',
    'cvat_adas_demo.restrictions',
    'cvat_adas_demo.lambda_manager',
    'cvat_adas_demo.opencv',
    'django_rq',
    'compressor',
    'cacheops',
    'sendfile',
    'dj_pagination',
    'revproxy',
    'rules',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'corsheaders',
    'allauth.socialaccount',
    'rest_auth.registration'
]

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'cvat_adas_demo.restrictions.serializers.RestrictedRegisterSerializer',
}

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'cvat_adas_demo.authentication.serializers.PasswordResetSerializerEx',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # FIXME
    # 'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'cvat_adas_demo.authentication.auth.TokenAuthentication',
        'cvat_adas_demo.authentication.auth.SignatureAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]}

# Django Auth
DJANGO_AUTH_TYPE = 'BASIC'
DJANGO_AUTH_DEFAULT_GROUPS = []
LOGIN_URL = 'rest_login'
LOGIN_REDIRECT_URL = '/'

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder',
# ]


UI_URL = ''

ROOT_URLCONF = 'cvat_adas_demo.urls'

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

SITE_ID=1


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 7000,
        'DB': 0,
        'DEFAULT-TIMEOUT': 360,
    }
}


WSGI_APPLICATION = 'cvat_adas_demo.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', 
    'django_auth_ldap.backend.LDAPBackend',
    
]

# https://github.com/pennersr/django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'
# set UI url to redirect after a successful e-mail confirmation
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/auth/login'
OLD_PASSWORD_FIELD_ENABLED = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'adas_cvat',
        'HOST': '127.0.0.1',
        'PORT': 27017,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logstash': {
            '()': 'logstash_async.formatter.DjangoLogstashFormatter',
            'message_type': 'python-logstash',
            'fqdn': False, # Fully qualified domain name. Default value: false.
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': [],
            'formatter': 'standard',
        },
        'server_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': os.path.join(BASE_DIR, 'logs', 'cvat_server.log'),
            'formatter': 'standard',
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'formatter': 'logstash',
            'transport': 'logstash_async.transport.HttpTransport',
            'ssl_enable': False,
            'ssl_verify': False,
            'host': os.getenv('DJANGO_LOG_SERVER_HOST', 'localhost'),
            'port': os.getenv('DJANGO_LOG_SERVER_PORT', 8080),
            'version': 1,
            'message_type': 'django',
            'database_path': 'LOGSTASH_DB',
          
        }
    },
    'loggers': {
        'cvat_adas_demo.server': {
            'handlers': ['console', 'server_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },

        'cvat_adas_demo.client': {
            'handlers': [],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },

        'revproxy': {
            'handlers': ['console', 'server_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
        },
        'django': {
            'handlers': ['console', 'server_file'],
            'level': 'INFO',
            'propagate': True
        }
    },
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
os.makedirs(STATIC_ROOT, exist_ok=True)

DATA_ROOT = os.path.join(BASE_DIR, 'data')
LOGSTASH_DB = os.path.join(DATA_ROOT,'logstash.db')
os.makedirs(DATA_ROOT, exist_ok=True)
if not os.path.exists(LOGSTASH_DB):
    open(LOGSTASH_DB, 'w').close()

MEDIA_DATA_ROOT = os.path.join(DATA_ROOT, 'data')
os.makedirs(MEDIA_DATA_ROOT, exist_ok=True)

CACHE_ROOT = os.path.join(DATA_ROOT, 'cache')
os.makedirs(CACHE_ROOT, exist_ok=True)

TASKS_ROOT = os.path.join(DATA_ROOT, 'tasks')
os.makedirs(TASKS_ROOT, exist_ok=True)

PROJECTS_ROOT = os.path.join(DATA_ROOT, 'projects')
os.makedirs(PROJECTS_ROOT, exist_ok=True)

SHARE_ROOT = os.path.join(BASE_DIR, 'share')
os.makedirs(SHARE_ROOT, exist_ok=True)

MODELS_ROOT = os.path.join(DATA_ROOT, 'models')
os.makedirs(MODELS_ROOT, exist_ok=True)

LOGS_ROOT = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_ROOT, exist_ok=True)

MIGRATIONS_LOGS_ROOT = os.path.join(LOGS_ROOT, 'migrations')
os.makedirs(MIGRATIONS_LOGS_ROOT, exist_ok=True)

CLOUD_STORAGE_ROOT = os.path.join(DATA_ROOT, 'storages')
os.makedirs(CLOUD_STORAGE_ROOT, exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
