#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint

from flask import request, session, redirect, url_for,\
    render_template, flash, make_response
import feedgenerator

from ..models import User, Entry


front = Blueprint('front', __name__)


@front.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@front.route('/about')
def about():
    return render_template('about.html')


@front.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('front.show_entries'))
    return render_template('login.html', error=error)


@front.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('front.show_entries'))


@front.route('/rss')
def rss_feed():

    feed = feedgenerator.Rss201rev2Feed(
        title="Rss from blog.zhongmoxi.com",
        link="blog.zhongmoxi.com",
        description="""Hi moxi""",
        language=u"zh-cn",
    )

    entries = Entry.query.all()
    for entry in entries:
        feed.add_item(
            title=entry.title,
            link="/entry/" + str(entry.id),
            description=entry.text,
        )
    feed = feed.writeString('UTF-8')
    resp = make_response(feed)
    resp.headers["Content-Type"] = "application/rss+xml"
    return resp
