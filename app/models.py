#!/usr/bin/env python3

import jwt
from flask import current_app as app
from . import db, login
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_contributor(id):
    return Contributor.query.get(int(id))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    contributor_id = db.Column(db.Integer, nullable=False)
    catid = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Task {}>'.format(self.id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    contributor_id = db.Column(db.Integer, nullable=False)
    hidden = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Contributor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    totp_key = db.Column(db.String(16))
    use_totp = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Contributor {}>'.format(self.name)

    def get_reset_password_token(self, expires_in=1800):
        token = jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')
        if type(token) == str:
            return token
        else:
            return token.decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
        return Contributor.query.get(id)


class EmailWhiteList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<EmailWhiteList {}>'.format(self.email)
