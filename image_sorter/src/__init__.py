import os

from flask import Flask


class Dependencies(object):
    def __init__(self):
        self.img_store = None

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

    from src.api.sort import sort_blueprint
    app.register_blueprint(sort_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
