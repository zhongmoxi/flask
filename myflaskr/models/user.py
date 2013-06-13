#!/usr/bin/env python
# encoding: utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(20))

    @classmethod
    def create(cls, username, password):
        user = cls()
        user.username = username
        user.set_password(password)
        return user

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
