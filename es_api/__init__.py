from flask import Flask
from . import blueprint_builder


def create_app(config_name):
    app = Flask(__name__)
    if config_name == "TESTING":
        from config import TestingConfig
        app.config.from_object("config.TestingConfig")
        bp = blueprint_builder.create_blueprint(TestingConfig)
    elif config_name == "PRODUCTION":
        from config import ProductionConfig
        app.config.from_object("config.ProductionConfig")
        bp = blueprint_builder.create_blueprint(ProductionConfig)
    else:
        raise ValueError("config name can be either TESTING or PRODUCTION")
    app.register_blueprint(bp)

    return app
