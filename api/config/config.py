import os
from decouple import config
from datetime import timedelta

# This is the base directory for the current file.
# It is used to get the directory path of the current file.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# this is the configuration class for the application
# it contains the configuration for the application
# it is used to configure the application
# it is used to configure the database
# it is used to configure the JWT
# it is used to configure the secret key
# it is used to configure the JWT secret key
# it is used to configure the JWT access token expiration
class Config:
    # this is the secret key for the application
    # this is gotten from the environment variable
    SECRET_KEY = config('SECRET_KEY', 'secret')
    # the expiration time for the access token is 30 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    # the expiration time for the refresh token is 30 days
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # the secret key for the JWT
    # this is gotten from the environment variable
    JWT_SECRET_KEY = 'iudsklpoiojknm,;lk'


class DevConfig(Config):
    # this is the configuration for the development environment
    # debug mode is enabled
    DEBUG = True
    # this is the configuration for the database
    # the tracking of the database is disabled
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # the sqlalchemy echo is enabled
    # this is used to log the database queries
    SQLALCHEMY_ECHO = True
    # the database uri is set to sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

# this is the dictionary that contains the configuration classes
config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}