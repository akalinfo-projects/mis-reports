
import logging
import os

import traceback
from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache
from flask_appbuilder.security.manager import AUTH_OAUTH
from authlib.integrations.flask_client import OAuth

#from superset.security import SupersetSecurityManager
#from flask_appbuilder.security.manager import AUTH_REMOTE_USER
from flask import request

logger = logging.getLogger()

        

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")
APP_NAME = "eNAM Analytics Dashboard"
APP_ICON = "/static/assets/images/enam_logo.png"
LOGO_TARGET_PATH = "https://uat.enam.gov.in/welcome"
LOGOUT_REDIRECT_URL = "https://uat.enam.gov.in/login"

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG



class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"  # When using docker compose baseurl should be http://superset_app:8088/
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
SQLLAB_CTAS_NO_LIMIT = True



# Ensure cookies work across subdomains and secure transport
#SESSION_COOKIE_SAMESITE = "None"
#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN", ".yourdomain.com")

###Keycloak integration details:

AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"  # Default role for new users


OAUTH_PROVIDERS = [{
    'name': 'keycloak',
    'icon': 'fa-key',
    'token_key': 'access_token',  # Token field in the response from Keycloak
    'remote_app': {
        'client_id': 'IAM-Service',  # Your Keycloak client ID
        'client_secret': 'GKd1fd3xLd61HYxbgECjfIUN337LLMDC',  # Your Keycloak client secret
        'api_base_url': 'https://keycloak-uat.enam.gov.in/realms/iamservice/protocol/',
        'access_token_url': 'https://keycloak-uat.enam.gov.in/realms/iamservice/protocol/openid-connect/token',
        'authorize_url': 'https://keycloak-uat.enam.gov.in/realms/iamservice/protocol/openid-connect/auth',
        'jwks_uri': 'https://keycloak-uat.enam.gov.in/realms/iamservice/protocol/openid-connect/certs',
        'client_kwargs': {
            'scope': 'openid email profile uma_authorization',
            'token_endpoint_auth_method': 'client_secret_post',
            'prompt':'none',
        },
         'userinfo_endpoint': 'https://keycloak-uat.enam.gov.in/realms/iamservice/protocol/openid-connect/userinfo',
    },
}]

    
# Map the incoming user information to Superset fields
OAUTH_USER_INFO = {
    "username": lambda d: d.get("preferred_username", ""),
    "email": lambda d: d.get("email", ""),
    "first_name": lambda d: d.get("given_name", ""),
    "last_name": lambda d: d.get("family_name", ""),
    "roles": lambda d: d.get("roles", []),
}   

# Redirect URI
OAUTH_REDIRECT_URI = "https://reports-uat.enam.gov.in/oauth-authorized/keycloak"


# CORS Configuration
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": ["https://reports-uat.enam.gov.in"],
}




    
###