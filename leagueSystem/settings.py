"""
Django settings for leagueSystem project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6b4sy&r&2tb05h4ed&$cdmpe6xj9r1jkfl#(yul6^j&%9d-z)t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.35', '127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'League.apps.LeagueConfig',
    'LeagueAPI.apps.LeagueAPIConfig',
    'rest_framework',
    'widget_tweaks',
    'smart_selects',
    'social_django',
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

ROOT_URLCONF = 'leagueSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'League.views.add_my_login_form',

            ],
        },
    },
]

WSGI_APPLICATION = 'leagueSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# JQUERY_URL = "/static/pinkhuge/wp-includes/jqueryb8ff.js"
# USE_DJANGO_JQUERY = True
USE_DJANGO_JQUERY = True
# JQUERY_URL = False

# CSP_DEFAULT_SRC = ("'none'",)
# CSP_STYLE_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'",)
# CSP_FONT_SRC = ("'self'",)
# CSP_IMG_SRC = ("'self'",)
#
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# ENVIRONMENT='production'
# URL CONFIG
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

# For conformation mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'furkanfbr@gmail.com'
EMAIL_HOST_PASSWORD = 'fur8989323846qQ@'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('static'),)
# STATIC_ROOT =os.path.join(BASE_DIR, 'static')
# SITE_URL = "http://127.0.0.1:8000"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',

    ),
}

######## STEAM AUTH #############
SOCIAL_AUTH_STEAM_API_KEY = 'BA270B7146A288C4A40DBF38E876E180'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    # others, if you want them...
)
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'League.steam.save_profile',
)
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']
