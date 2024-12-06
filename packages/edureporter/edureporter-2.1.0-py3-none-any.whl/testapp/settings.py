import os
from pathlib import (
    Path,
)

import django

from edureporter.storage import (
    REPORTS_STORAGE_ALIAS,
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mc^jjzr_7emr)s#k%$2_g3z_odvzj-%sye1ho42l6v_8l+(mov'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'testapp.app',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'testapp.urls'

local_template_packages = (
    ('testapp', None),
    ('testapp', 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': list(set(
            (
                os.path.join(path, relative_path)
                if relative_path else
                os.path.dirname(path)
            )
            for name, relative_path in local_template_packages
            for path in __import__(name).__path__
        )),
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ])
            ]
        }
    }
]


WSGI_APPLICATION = 'testapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'testapp'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': 5432,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

REPORTS_DIR = Path(MEDIA_ROOT) / 'downloads' / 'reports'
REPORTS_URL = f'{MEDIA_URL}downloads/reports'

if django.VERSION >= (4, 2):
    STATIC_STORAGE = {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        'OPTIONS': {
            'location': STATIC_ROOT,
            'base_url': STATIC_URL
        }
    }

    MEDIA_STORAGE = {
        'BACKEND': 'django.core.files.storage.filesystem.FileSystemStorage',
        'OPTIONS': {
            'location': MEDIA_ROOT,
            'base_url': MEDIA_URL,
        }
    }

    REPORTS_STORAGE = {
        'BACKEND': 'edureporter.storage.ReportsStorage',
        'OPTIONS': {
            'location': Path(MEDIA_ROOT) / 'downloads' / 'reports',
            'base_url': f'{MEDIA_URL}downloads/reports',
        }
    }

    STORAGES = {
        'default': MEDIA_STORAGE,
        'staticfiles': STATIC_STORAGE,
        REPORTS_STORAGE_ALIAS: REPORTS_STORAGE
    }


# Настройки Брокера ()
BROKER_URL = 'redis://localhost:6379/11'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/11'
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_TIMEZONE = TIME_ZONE
CELERY_USE_UTC = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'zeep': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
