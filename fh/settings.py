"""
Django settings for fh project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
from os import environ as env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# fake out gettext
gettext = lambda s: s

import dj_database_url


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'v(orw(@bjr!^qq1psc*38p=_q#c_@h20+yr$5je7t1jd!l5%l$'
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']
ADMINS = ['greg@kempe.net']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition
ROOT_URLCONF = 'fh.urls'

# we server multiple websites based on domain
ROOT_HOSTCONF = 'fh.hosts'
DEFAULT_HOST = 'www'

WSGI_APPLICATION = 'fh.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///development.sqlite3')
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Applications
INSTALLED_APPS = (
    # cms admin
    'djangocms_admin_style',
    'djangocms_text_ckeditor',

    # django core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',

    # store stuff in s3
    'storages',

    # cms core
    'cms',
    'mptt',
    'menus',
    'south',
    'sekizai',
    'reversion',

    # Asset pipeline
    'compressor',

    # cms plugins
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',

    # choose URLs based on domains
    'django_hosts',

    # us
    'fh',
)

MIDDLEWARE_CLASSES = (
    'django_hosts.middleware.HostsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'fh', 'static'),
)


# Media uploads
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests

AWS_S3_ACCESS_KEY_ID = env.get('AWS_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = env.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'freedom-house-media'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Templates
TEMPLATE_DEBUG = DEBUG
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings',
    'lib.context_processors.google_analytics',
    'lib.context_processors.speakup',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'fh', 'templates'),
)


# Speak Up Mzansi

SPEAKUP_DISCOURSE_URL = 'http://speakupmzansi.org.za'
SPEAKUP_DISCOURSE_USERNAME = env.get('DISCOURSE_USERNAME')
SPEAKUP_DISCOURSE_API_KEY = env.get('DISCOURSE_API_KEY')

SPEAKUP_INFO_URL      = 'http://info.speakupmzansi.org.za' # this site


# Google Analytics
GOOGLE_ANALYTICS_TRACKING_ID = env.get('DJANGO_GOOGLE_ANALYTICS_TRACKING_ID')
GOOGLE_ANALYTICS_DOMAIN = env.get('DJANGO_GOOGLE_ANALYTICS_DOMAIN')


# MXit
MXIT_CLIENT_ID = env.get('MXIT_CLIENT_ID')
MXIT_SECRET = env.get('MXIT_SECRET')


# asset pipeline
COMPRESS_OFFLINE = env.get('DJANGO_COMPRESS_OFFLINE') == 'true'
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'GOOGLE_ANALYTICS_TRACKING_ID': GOOGLE_ANALYTICS_TRACKING_ID,
    'GOOGLE_ANALYTICS_DOMAIN': GOOGLE_ANALYTICS_DOMAIN,
}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter'
]


# CMS config
CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    ('page.html', 'Simple page'),
    ('cms_twocolumn.html', 'Two column page'),
    ('cms_threecolumn.html', 'Three column page'),
    ('feature.html', 'Page with Feature')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'fh': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
