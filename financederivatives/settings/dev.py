from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-t%!plxq5z3fg8xl_yq#xxgfo$6%erfn@m^j0mq^_c&&z)(-5q4"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'y.ibork1@gmail.com'
EMAIL_HOST_PASSWORD = 'ccdawixitxpgoxeh'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'y.ibork1@gmail.com'
EMAIL_BACKEND = 'joblistings.backends.NoVerifyEmailBackend'



try:
    from .local import *
except ImportError:
    pass
