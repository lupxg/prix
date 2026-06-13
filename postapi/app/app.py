from flask import Flask
from app.extensions import db, migrate
from flask_restx import Api
from .routes import register_routes

authorizations = {'Bearer': {'type':'apiKey', 'in':'header','name':'Authorization'}}

def create_app(config_override=None):
    """
    Create a Flask application using the app factory pattern

    :return: Flask app 
    """

    app  = Flask(__name__)
    app.config.from_object("app.config")

    if config_override:
        app.config.update(config_override)

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions.

    :param api: API RESTx instance
    :param app: Flask application instance
    :return: None
    """
    api = Api(
        title='smallpost',
        version='1.0',
        description='Lightweight posts system',
        authorizations=authorizations,
        security='Bearer'
    )

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    register_routes(api, app, 'spost')

    with app.app_context():
        db.create_all()

    return None


if __name__ == '__main__':
    app = create_app()
    app.run()
