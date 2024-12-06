"""
Application Factory
===================

This module provides a factory function for creating and configuring a Flask application.

Functions:
    - create_app(config_name=None, summary_service=None): Creates and configures a Flask application instance.
"""

from flasgger import Swagger
from flask import Flask

from t1cicd.cicd.api.api import register_routes
from t1cicd.cicd.api.config import DevelopmentConfig, ProductionConfig, TestingConfig
from t1cicd.cicd.db.db import init_flask_db
from t1cicd.cicd.db.service.summary import SummaryService


def create_app(config_name=None, summary_service=None):
    """
    Creates and configures a Flask application instance.

    This factory function sets up the application configuration, initializes Swagger for API documentation,
    sets up the database (unless in testing mode), and registers routes for the application.

    Args:
        config_name (str, optional): The name of the configuration to use. Defaults to "development".
                                      Options are "development", "testing", or "production".
        summary_service (SummaryService, optional): An instance of the summary service to inject into the app.
                                                    If not provided, a new instance will be created.

    Returns:
        Flask: A configured Flask application instance.

    Example:
        >>> from factory import create_app
        >>> app = create_app(config_name="production")
    """
    app = Flask(__name__)

    # Choose the configuration based on the provided config name
    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)  # Default to development config

    # Initialize Swagger
    Swagger(app)

    # Initialize the database (but skip in tests)
    if config_name != "testing":
        init_flask_db(app)
        summary_service = SummaryService()

    # Register routes from api.py
    register_routes(app, summary_service)

    return app
