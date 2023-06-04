from flask.cli import FlaskGroup

from flask_sqlalchemy import SQLAlchemy

from src import create_app, dependencies, Dependencies
from src.api.models import Image
from src.store import FileSystemStore


def _create_app():
    deps = Dependencies()
    deps.set_img_store(FileSystemStore('/data/'))
    return create_app(deps)


cli = FlaskGroup(create_app=_create_app)


@cli.command('recreate_db')
def recreate_db():
    dependencies.db.drop_all()
    dependencies.db.create_all()
    dependencies.db.session.commit()

@cli.command('seed_db')
def seed_db():
    dependencies.db.session.add(Image(path='a.jpg'))
    dependencies.db.session.add(Image(path='b.png'))
    dependencies.db.session.commit()

if __name__ == '__main__':
    cli()
