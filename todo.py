# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash
from contextlib import closing

import time

# configuration
DATABASE = 'todo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create the application
app = Flask(__name__)
app.config.from_object(__name__)


# database connectivity functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# page routing functions
@app.route('/index')
@app.route('/')
def show_todos():
    todos = query_db('select * from todo order by id desc')
    return render_template('todos.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    get_db().execute('insert into todo (description, due_date) values (?, ?)',
                    [request.form['description'], request.form['due_date']])
    get_db().commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_todos'))

@app.route('/ajax_call', methods=['POST'])
def update_todo():
    get_db().execute('update todo set done = ?, finished_ts = ? where id= ?', [int(request.json['is_done']), str(time.strftime("%d %m %Y")), int(request.json['id'])])
    get_db().commit()
    flash('updated')

    return redirect(url_for('show_todos'))

# main function
if __name__ == '__main__':
    app.run()