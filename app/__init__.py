#!/usr/bin/env python3

import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
mail = Mail()


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from app.sendxmpp_handler import SENDXMPPHandler

    if app.config['LOGGING_XMPP_SERVER']:
        sendxmpp_handler = SENDXMPPHandler(
            logging_xmpp_server=(app.config['LOGGING_XMPP_SERVER']),
            logging_xmpp_sender=(app.config['LOGGING_XMPP_SENDER']),
            logging_xmpp_password=(app.config['LOGGING_XMPP_PASSWORD']),
            logging_xmpp_recipient=(app.config['LOGGING_XMPP_RECIPIENT']),
            logging_xmpp_command=(app.config['LOGGING_XMPP_COMMAND']),
            logging_xmpp_use_tls=(app.config['LOGGING_XMPP_USE_TLS']),
        )
        sendxmpp_handler.setLevel(logging.ERROR)
        app.logger.addHandler(sendxmpp_handler)

    from .tasks import tasks, new_task, task_action, edit_task
    from .tasks import delete_move_toggle_task, reorder_priorities
    from .categories import hide_categories, delete_category
    from .categories import new_category, categories
    from .auth import auth, profile, reset_password, register, totp
    with app.app_context():
        app.register_blueprint(categories.cats)
        app.register_blueprint(new_category.new_cat)
        app.register_blueprint(hide_categories.hidecats)
        app.register_blueprint(delete_category.delcat)
        app.register_blueprint(auth.auths)
        app.register_blueprint(profile.prof)
        app.register_blueprint(reset_password.pwd)
        app.register_blueprint(register.reg)
        app.register_blueprint(totp.totps)
        app.register_blueprint(tasks.tsks)
        app.register_blueprint(new_task.newtask)
        app.register_blueprint(task_action.taskaction)
        app.register_blueprint(edit_task.edittask)
        app.register_blueprint(delete_move_toggle_task.deletetask)
        app.register_blueprint(delete_move_toggle_task.toggletaskdone)
        app.register_blueprint(delete_move_toggle_task.movecat)
        app.register_blueprint(reorder_priorities.reorderp)

        return app
