from flask.cli import FlaskGroup

from src import create_app,Dependencies
from src.store import RemoteImageResolver


def _create_app():
    deps = Dependencies()
    deps.set_img_store(RemoteImageResolver('smart-paletter-image-store-1', 5000))
    return create_app(deps)


cli = FlaskGroup(create_app=_create_app)


if __name__ == '__main__':
    cli()
