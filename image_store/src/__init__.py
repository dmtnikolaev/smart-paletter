import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Dependencies(object):
    def __init__(self):
        self.img_store = None
        self.db = SQLAlchemy()

    def update(self, dep):
        self.set_img_store(dep.img_store)

    def set_img_store(self, img_store):
        self.img_store = img_store


dependencies = Dependencies()


def create_app(deps, script_info=None):
    dependencies.update(deps)

    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    dependencies.db.init_app(app)

    from src.api.imgs import images_blueprint
    app.register_blueprint(images_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': dependencies.db}

    return app
