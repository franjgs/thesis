import djcelery
from os.path import expanduser
from web import config
from datetime import timedelta

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (config.ADMIN_NAME, config.ADMIN_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': config.ENGINE,
        'NAME': config.NAME,
        'USER': config.USER,
        'PASSWORD': config.PASSWORD,
        'HOST': config.HOST,
        'PORT': config.PORT,
    }
}

HOSTNAME = config.HOSTNAME

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'static/'

# Additional locations of static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.SECRET_KEY

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'web.urls'

# Settings for machine learning models
N_MODELS = 5

# Maximum number of tweets to fetch in a single request
MAX_TWEETS = 100

# Maximum number of stories to fetch (from each subreddit) in a single request
MAX_STORIES = 500
SUBREDDITS = [ "suicidewatch", "happy" ]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'web.wsgi.application'

TEMPLATE_DIRS = (
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'ratings',
    'monitor',
    'south',
    'djcelery',
    'kombu.transport.django',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

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

# django-celery
djcelery.setup_loader()
BROKER_URL = "django://"
CELERY_IMPORTS = (
    'ratings.tasks',
    'monitor.tasks',
)
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "mysql://" + config.USER + ":" + config.PASSWORD + "@localhost/" + config.NAME
CELERY_ANNOTATIONS = { "tasks:add": { "rate_limit": "10/s" } }
CELERYBEAT_SCHEDULE = {
    'runs-every-3-hours': {
        'task': 'monitor.tasks.fetch_from_twitter',
        'schedule': timedelta(hours = 3),
        'args': ()
    }
}
CELERY_TIMEZONE = 'Europe/Berlin'
CELERYD_NODES = "w1"
CELERYD_LOG_FILE = expanduser("~") + "/system/celeryd.log"
