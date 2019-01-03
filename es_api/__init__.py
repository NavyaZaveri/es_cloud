from flask import Flask

from . import blueprint_builder
from config import ProductionConfig
from config import TestingConfig


def create_app(config_name):
    app = Flask(__name__)
    if config_name == "TESTING":
        app.config.from_object("config.TestingConfig")
        bp = blueprint_builder.create_blueprint(TestingConfig)
    else:
        app.config.from_object("config.ProductionConfig")
        bp = blueprint_builder.create_blueprint(ProductionConfig)
    if bp is None:
        raise ValueError("config name can be either TESTING or PRODUCTION")
    app.register_blueprint(bp)

    return app
