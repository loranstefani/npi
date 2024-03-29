# Django settings for npi project.
import os

from django.contrib.messages import constants as messages

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitestatic'),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '29s(+yuh#r)#)bpv=67e)!=-3^_1a#rldyzmvc0jkxg25$83*u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.transaction.TransactionMiddleware',
    #'reversion.middleware.RevisionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.middleware.XForwardedForMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'npi.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'npi.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    
    #3rd party
    'ajax_select',
    'bootstrapform',
    'localflavor',
    'django_extensions',
    'reversion',
    
    #npi apps
    'apps.accounts',
    'apps.taxonomy',
    'apps.enumerations',
    'apps.licenses',
    'apps.specialties',
    'apps.addresses',
    'apps.direct',
    'apps.identifiers',
    'apps.home',
    'apps.profilee',
    'apps.surrogates',
    'apps.downloads',
    'apps.statistics',
    'apps.reports',
    'apps.dmf',
    'apps.email_campaign',
    'apps.api',
    
    )


AJAX_LOOKUP_CHANNELS = {
    'address' : {'model':'addresses.Address', 'search_field':'address_1',
                  'min_length': '5'
                 },
    'license' : {'model':'licenses.License', 'search_field':'number',
                 'min_length': '4'},
        
    'identifier' : {'model':'identifiers.Identifier', 'search_field':'identifier',
                 'min_length': '4'},    
    'manager' : {'model':'auth.User', 'search_field': 'email',
                 'min_length': '4'},   
    'direct' : {'model':'direct.DirectAddress', 'search_field': 'email',
               'min_length': '5' },
    'enumeration' : {'model':'enumerations.Enumeration', 'search_field': 'handle',
                     'min_length': '5'},
    }



LUHN_PREFIX ="80840"
VERIFY_LUHN_AND_UNIQUE_ENUMERATION = False
GATEKEEPER = True
AUTO_ENUMERATION_USERNAME = "system"

ANTI_VIRUS = False


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



MESSAGE_TAGS ={messages.DEBUG: 'debug',
messages.INFO: 'info',
messages.SUCCESS: 'success',
messages.WARNING: 'warning',
messages.ERROR: 'danger',}

# To enable your own local settings.
# Copy file found in settings_local_example.py to settings_local.py.
# Place this file in ithe same directory as settings.py

# Twilio SMS Settings -----------------------------------------------
TWILIO_DEFAULT_FROM = "+15555555555"
TWILIO_API_BASE = "https://api.twilio.com/2010-04-01"
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_API_VERSION = '2010-04-01'
SMS_LOGIN_TIMEOUT_MIN = 10

EMAIL_HOST_USER = 'email_from@example.com'
HOSTNAME_URL = 'http://127.0.0.1:8000'
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
SEND_EMAIL = False
MIN_PASSWORD_LEN =8
ORGANIZATION_NAME = "NPPES"
INVITE_REQUEST_ADMIN = "someone@example.com"


UPDATE_LAST_UPDATE_DATE = True #Set this to False in settings_local when importing legacy data.

AUTH_PROFILE_MODULE = 'accounts.userprofile'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)


try:
    from settings_local import *
except:
    pass

