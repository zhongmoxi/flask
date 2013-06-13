#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint
from flask import request, session, redirect, url_for,\
    abort, render_template, flash

from ..models import db, Entry

en = Blueprint('entry', __name__)


@en.route('/<int:entry_id>')
def entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return abort(404)
    return render_template('entry.html', entry=entry)


@en.route('/<int:entry_id>/edit', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.query.get(entry_id)
    if request.method == 'GET':
        return render_template('edit_entry.html', entry=entry)
    else:
        entry.title = request.form['title']
        entry.text = request.form['text']
        db.session.commit()
        flash('entry was successfully updated')
        return redirect(url_for('entry.entry', entry_id=entry.id))


@en.route('/<int:entry_id>/delete', methods=['GET'])
def delete_entry(entry_id):
    if not session.get('logged_in'):
        abort(401)
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('New entry was successfully deleted')
    return redirect(url_for('front.show_entries'))


@en.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    author = session['username']
    text = request.form['text']
    en = Entry.create(title, author, text)
    db.session.add(en)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('front.show_entries'))
