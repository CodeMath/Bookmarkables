from datetime import timedelta

# from secret_keys import CSRF_SECRET_KEY, SESSION_KEY


class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = "asgwrgokopbsadaw3"
    # CSRF_SESSION_KEY = SESSION_KEY
    debug = False
    PERMANENT_SESSION_LIFETIME=timedelta(days=30)



class Production(Config):
    DEBUG = True
    CSRF_ENABLED = False
    ADMIN = ""
    SQLALCHEMY_DATABASE_URI = ''
    migration_directory = 'migrations'


class FacebookAPI():
    SECRET_KEY = ""
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET = ''
    debug = True
