# all the imports
from __future__ import with_statement
from contextlib import closing
import sqlite3
import time
from flask import Flask,request,session,g,redirect,url_for,\
     abort,render_template,flash
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


# configuration

#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

# create our litter application :)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/flask.db'
db = SQLAlchemy(app)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author = db.Column(db.String(20))
    pub_date =db.Column(db.DateTime)
    #time=db.Column(db.String(30))   
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username 
        self.set_password(password)

    def set_password(self,password):
	self.password = generate_password_hash(password)
    
    def check_password(self,password):
	return check_password_hash(self.password,password)

    def __repr__(self):
        return '<User %r>' % self.username

#def connect_db():
#    return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql') as f:
#	    db.cursor().executescript(f.read())
#	db.commit() 

#@app.before_request
#def before_request():
#    g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
#    g.db.close()

@app.route('/')
def show_entries():
#    cur = g.db.execute('select title,author,time,text from entries order by id desc')
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add', methods=['POST'])
def add_entry():
    #cur_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if not session.get('logged_in'):
	abort(401)
    #g.db.execute('insert into entries (title,author,time, text) values (?, ?, ?, ?)',[request.form['title'],app.config['USERNAME'],cur_time,request.form['text']])
    title=request.form['title']
    author = session['username']
    text=request.form['text']
    en=Entry(title,author,text)
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

if __name__ == '__main__':
    app.run()
 

