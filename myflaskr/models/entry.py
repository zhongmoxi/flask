#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime

from .db import db


class Entry(db.Model):

    __searchable__ = ['text']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(20))
    pub_date = db.Column(db.DateTime)
    text = db.Column(db.String(100))

    @classmethod
    def create(cls, title, author, text, pub_date=None):
        entry = cls()
        entry.title = title
        entry.author = author
        entry.text = text
        if pub_date is None:
            pub_date = datetime.now()
        entry.pub_date = pub_date
        return entry

    def __repr__(self):
        return '<Post %r>' % self.title
