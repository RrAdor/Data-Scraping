"""
Django settings for newsarticle project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-_u3yusyh!+d*zu0&ssug9ykaze5yuusff9=b0)=jedi-x=$&s#'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Adjust for production

# Application definition - Minimal apps needed for messaging
INSTALLED_APPS = [
    'django.contrib.sessions',     # Required for messages
    'django.contrib.messages',     # Required for messages
    'django.contrib.staticfiles',  # For static assets
    'newsapp',
]

# Middleware - Added back message middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for messages
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # For messaging
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Disable database and auth systems
DATABASES = {}
AUTHENTICATION_BACKENDS = []
AUTH_PASSWORD_VALIDATORS = []

ROOT_URLCONF = 'newsarticle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # This line is crucial
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# MongoDB Configuration
# MongoDB Configuration
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'scrapy_news'  # Should match your Scrapy settings

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Disable default auto field
DEFAULT_AUTO_FIELD = None

# Session settings - using signed cookies instead of database
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True

# Message storage using sessions
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'