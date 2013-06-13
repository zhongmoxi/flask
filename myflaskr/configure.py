#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

from .models import db, User, Entry
from .views import configure_blueprint
from .helpers import configure_helpers


# create our litter application :)
def configure_app(app):
    db.init_app(app)
    configure_blueprint(app)
    configure_helpers(app)
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Entry, db.session))
    return app
