# -*- coding:utf-8  -*-
from flask import Flask
from app.modules import init_app
from app.controllers.database import init_db
from app.modules.chat_bot import init_chat_bot
from app.modules.arduino import init_arduino
from app.modules.services import init_services


def create_app():
    app: Flask = Flask(__name__)
    app.config.from_object('configFlask')

    init_db(app)
    init_app(app)
    init_services(app)
    init_chat_bot(app)
    init_arduino(app)

    return app
