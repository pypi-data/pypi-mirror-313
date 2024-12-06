"""
Run Server
==========

This script initializes and runs the CI/CD server using the Flask application factory.

Functions:
    - main(): Initializes the application with the specified configuration and starts the server.
"""

from t1cicd.cicd.api.factory import create_app


def main():
    """
    Initializes the Flask application with the development configuration and runs the server.

    The application is created using the `create_app` function from the factory module.
    Debug mode is disabled for this setup.

    Example:
        To start the server, run this script:
            $ python run.py
    """
    # Pass the desired configuration when creating the app
    app = create_app(config_name="DevelopmentConfig")
    app.run(debug=False)
