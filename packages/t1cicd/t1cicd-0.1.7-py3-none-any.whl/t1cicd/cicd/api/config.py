"""
Configuration Module
====================

This module defines configuration classes for different environments: development, testing, and production.

Classes:
    - Config: Base configuration class with common settings.
    - DevelopmentConfig: Configuration for development environment.
    - TestingConfig: Configuration for testing environment.
    - ProductionConfig: Configuration for production environment.
"""


class Config:
    """
    Base configuration class.

    Attributes:
        DEBUG (bool): Whether to enable debug mode. Defaults to False.
        TESTING (bool): Whether to enable testing mode. Defaults to False.
        DATABASE_URI (str): URI for the database connection. Defaults to "postgresql://user@localhost/dbname".
        SECRET_KEY (str): Secret key for the application. Defaults to "your_secret_key".
    """

    DEBUG = False
    TESTING = False
    DATABASE_URI = "postgresql://user@localhost/dbname"
    SECRET_KEY = "your_secret_key"


class DevelopmentConfig(Config):
    """
    Configuration for the development environment.

    Inherits from:
        Config

    Overrides:
        TESTING: False
        DEBUG: False
        DATABASE_URI: "postgresql://dev_user@localhost/dev_dbname"
    """

    TESTING = False
    DEBUG = False
    DATABASE_URI = "postgresql://dev_user@localhost/dev_dbname"


class TestingConfig(Config):
    """
    Configuration for the testing environment.

    Inherits from:
        Config

    Overrides:
        TESTING: True
        DEBUG: True
        DATABASE_URI: "postgresql://test_user@localhost/test_dbname"
        SECRET_KEY: "test_secret"
    """

    TESTING = True
    DATABASE_URI = "postgresql://test_user@localhost/test_dbname"
    DEBUG = True
    SECRET_KEY = "test_secret"


class ProductionConfig(Config):
    """
    Configuration for the production environment.

    Inherits from:
        Config

    Overrides:
        DATABASE_URI: "postgresql://prod_user@localhost/prod_dbname"
        SECRET_KEY: "prod_secret"
    """

    DATABASE_URI = "postgresql://prod_user@localhost/prod_dbname"
    SECRET_KEY = "prod_secret"
