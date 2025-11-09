from pathlib import Path
from decouple import config, Csv
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config('SECRET_KEY', default='your-default-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # For TokenAuthentication
    'corsheaders',

    # apps
    "users",
    'nurses',
    'patients',
    'appointments',
    'authentications',
    'billing',
    'reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# PostgreSQL Database


DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default='postgresql://ehr_0xun_user:ri3Rd7m0fnNUaIHAcqBaN53dM5A2dSbN@dpg-d488o5ali9vc7395h5eg-a.oregon-postgres.render.com/ehr_0xun'
        ),
        conn_max_age=600,
        ssl_require=True
    )
}





# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # production frontend(s) - replace with your actual frontend URL
    "https://eldorethomebasedcare.netlify.app",
    "https://eldorethomecare.co.ke", 
]

# allow sending credentials from frontend
CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = 'users.User'

# CSRF Trusted Origins
# - include your deployed backend (https) and local dev hosts (http://localhost:8000)
CSRF_TRUSTED_ORIGINS = [
    "https://homebasedcarebackend.onrender.com",
    "https://eldorethomebasedcare.netlify.app",            # production frontend
    "https://eldorethomecare.co.ke",
    "http://127.0.0.1:8000",                       # local backend dev
    "http://localhost:8000",
    "http://127.0.0.1:3000",                       # local frontend dev ✅
    "http://localhost:3000",                       # local frontend dev ✅
]

# -----------------------------
# Cookie security settings
# -----------------------------
# Use secure cookies only when DEBUG is False (production). This allows local testing over HTTP.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# For local development we'll use "Lax" (safer than None) so cookies work on http://localhost:8000.
# In production you likely need "None" if frontend and backend are on different domains and you
# intentionally want cross-site cookies (and both use HTTPS).
SESSION_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"
CSRF_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"

# Keep cookies httpOnly (recommended)
SESSION_COOKIE_HTTPONLY = True

# During development you can allow all origins by uncommenting:
# CORS_ALLOW_ALL_ORIGINS = DEBUG
