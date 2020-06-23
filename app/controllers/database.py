from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask import Flask
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def init_db(app: Flask):

    db.init_app(app)

    Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    login_manager.init_app(app)
