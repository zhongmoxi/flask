#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import markdown
from flask import Flask, request, session, redirect, url_for,\
    abort, render_template, flash, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import flask.ext.whooshalchemy as whooshalchemy


# configuration

# DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

# create our litter application :)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/flask.db'
db = SQLAlchemy(app)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['WHOOSH_BASE'] = '/tmp/flask_search.db'
app.config['MAX_SEARCH_RESULTS'] = 50


class Entry(db.Model):

    __searchable__ = ['text']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(20))
    pub_date = db.Column(db.DateTime)
    # time=db.Column(db.String(30))
    text = db.Column(db.String(100))

    def __init__(self, title, author, text, pub_date=None):
        self.title = title
        self.author = author
        self.text = text
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


whooshalchemy.whoosh_index(app, Entry)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


@app.template_filter('md')
def md_filter(s):
    return Markup(markdown.markdown(s))


@app.template_filter()
def timesince(dt, default=u"刚刚"):

    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt

    periods = (
        (diff.days / 365, u" 年"),
        (diff.days / 30, u" 月"),
        (diff.days / 7, u" 周"),
        (diff.days, u" 天"),
        (diff.seconds / 3600, u" 小时"),
        (diff.seconds / 60, u" 分钟"),
    )

    for period, unit in periods:
        if period > 0:
            return u"%d%s前" % (period, unit)

    if diff.seconds > 1:
            return u"%d 秒前" % diff.seconds

    return default


@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    author = session['username']
    text = request.form['text']
    en = Entry(title, author, text)
    db.session.add(en)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            flash('Invalid username')
        elif not user.check_password(request.form['password']):
            flash('Invalid password')
        else:
            session['logged_in'] = True
            session['username'] = user.username
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/search', methods=['POST'])
def search():
    return redirect(url_for('search_results', query_word=request.form['query_word']))

@app.route('/search_results/<query_word>')
def search_results(query_word):
    results = Entry.query.whoosh_search(query_word,app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('search_results.html', query_word=query_word, results=results)

if __name__ == '__main__':
    app.run(debug=True)
