"""
Settings de production pour Site Web Help Robot
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Configuration des hosts autorisés
def get_allowed_hosts():
    """Récupère les hosts autorisés depuis les variables d'environnement"""
    allowed_hosts = []
    
    # Hosts depuis la variable d'environnement
    env_hosts = os.environ.get('ALLOWED_HOSTS', '')
    if env_hosts:
        allowed_hosts.extend([host.strip() for host in env_hosts.split(',') if host.strip()])
    
    # IP du serveur
    server_ip = os.environ.get('SERVER_IP')
    if server_ip and server_ip not in allowed_hosts:
        allowed_hosts.append(server_ip)
    
    # Domaine personnalisé si défini
    custom_domain = os.environ.get('CUSTOM_DOMAIN')
    if custom_domain and custom_domain not in allowed_hosts:
        allowed_hosts.append(custom_domain)
    
    # Hosts par défaut pour le développement/test
    default_hosts = ['localhost', '127.0.0.1', '0.0.0.0']
    for host in default_hosts:
        if host not in allowed_hosts:
            allowed_hosts.append(host)
    
    return allowed_hosts

ALLOWED_HOSTS = get_allowed_hosts()

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # Ajoutez vos apps tierces ici
]

LOCAL_APPS = [
    # Ajoutez vos apps locales ici
    # 'your_app',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'help_robot_db'),
        'USER': os.environ.get('DB_USER', 'help_robot_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
        'CONN_MAX_AGE': 60,
    }
}

# Password validation
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
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings pour la production
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = False  # Pas de HTTPS forcé car pas de nginx
    SECURE_PROXY_SSL_HEADER = None
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Session security
    SESSION_COOKIE_SECURE = False  # Pas de HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 3600  # 1 heure
    
    # CSRF protection
    CSRF_COOKIE_SECURE = False  # Pas de HTTPS
    CSRF_COOKIE_HTTPONLY = True

# Cache configuration (optionnel)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'myproject': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Créer le répertoire de logs s'il n'existe pas
log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)

# Configuration email (optionnel)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@helprobot.local')

# Configuration pour les fichiers statiques en production
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Affichage des informations de configuration (seulement en mode DEBUG)
if DEBUG:
    print(f"🔧 Configuration Django Production:")
    print(f"   - Hosts autorisés: {ALLOWED_HOSTS}")
    print(f"   - Base de données: {DATABASES['default']['ENGINE']}")
    print(f"   - IP du serveur: {os.environ.get('SERVER_IP', 'Non définie')}")
    print(f"   - Debug: {DEBUG}")