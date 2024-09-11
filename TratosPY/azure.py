from .settings import *
from .settings import BASE_DIR
import os

WIBBLE2 = 'Wibble2'


# TO-DO ADD IT CSRF_TRUSTED_ORIGINS = ['https://*'] as wildcar locally
# TO-DO once deployed from VS code
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://tratosweb.azurewebsites.net','*']
DEBUG = True

# TO-ADD -- uncomment

#add the next middleware for whitenoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enables whitenoise for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }   
}


#TO-DO add the static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


WHITENOISE_MANIFEST_STRICT = False
