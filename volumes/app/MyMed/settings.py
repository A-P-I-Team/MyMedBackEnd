"""
Django settings for MyMed project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent







# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY',default='a5ds16sa1f5as1d51a5sf135as1d5a1sf5a1sd5a1s561a4sf8as1f5asf6as1d65a1sd')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mymed.pythonanywhere.com','localhost','app']
CSRF_TRUSTED_ORIGINS=['http://localhost','http://mymed.pythonanywhere.com']
# CSRF_COOKIE_SECURE=False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    #auth token
    'rest_framework.authtoken',

    #THIRD_PARTY_LIBS:
        #swagger
        'drf_yasg',
        'django_nose',

        #django-filter
        'django_filters',

    #User app
    'User.apps.UserConfig',
    #Doc And Patient app
    'DocAndPatient.apps.DoctorAndPatientConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyMed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'MyMed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MARIADB_DATABASE'),
        'USER': os.environ.get('MARIADB_USER'),
        'PASSWORD': os.environ.get('MARIADB_PASSWORD'),
        'HOST': os.environ.get('MARIADB_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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






REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
       'rest_framework.authentication.BasicAuthentication',
    #    'rest_framework.authentication.SessionAuthentication',
   ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
   ),
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}









# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')


MEDIA_URL = 'media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

#must change for docker





# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'







EMAIL_BACKEND =config('EMAIL_BACKEND',default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST',default='smtp.gmail.com')
EMAIL_USE_TLS = config('EMAIL_USE_TLS',default=True)
EMAIL_PORT = config('EMAIL_PORT',default='587')
EMAIL_HOST_USER = config('EMAIL_HOST_USER',default='example@example.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD',default='examplepassword')


SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False
}






AUTH_USER_MODEL="User.User"


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=User',
]



CELERY_BROKER_URL = 'redis://redis:6379/0'




