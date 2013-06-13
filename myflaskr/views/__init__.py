#!/usr/bin/env python
# encoding: utf-8


def configure_blueprint(app):
    from .front import front
    from .entry import en
    app.register_blueprint(front, url_prefix="")
    app.register_blueprint(en, url_prefix="/entry")
