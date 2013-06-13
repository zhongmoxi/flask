#!/usr/bin/env python
# encoding: utf-8
import os
from flask import Flask
from flask.ext.script import Manager, prompt


from myflaskr.configure import configure_app

SECRET_KEY = 'asd%s*sdf'


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flaskr.db')
    configure_app(app)
    return app


app = create_app()
manager = Manager(app)


@manager.command
def syncdb():
    from myflaskr.models import db, User
    db.create_all()
    name = prompt("Enter user name")
    password = prompt("Enter password")
    user = User.create(name, password)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
