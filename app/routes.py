from flask import render_template, url_for, redirect
from app import app
from app.forms import TodoForm

import mysql.connector

def getdb_connection():
    """create db connection to sql database with ssl_disabled"""
    return mysql.connector.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        password = app.config['MYSQL_PASSWORD'],
        database = app.config['MYSQL_DB'],
        ssl_disabled = True
    )


@app.route('/')
@app.route('/index')
def index():
    # get form
    form = TodoForm()
    # create db connection
    cnx = getdb_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM todo")
    todos = cursor.fetchall()
    cursor.close()
    cnx.close()
    print(todos)
    return render_template('index.html',title='Todo List', todos=todos, form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = TodoForm()
    # submit form
    if form.validate_on_submit():
        # take data from and store as varaible
        todo = form.todo.data
        # connect to db
        cnx = getdb_connection()
        cursor = cnx.cursor()
        # ATTENTION!!!!
        # i should exclude id since it autoincrement in db
        # i need to send as tuple or list so i must write it as tuple
        # (todo,) make it a tuple
        # finally if i dont use small letter %s it will not work

        cursor.execute("INSERT INTO todo (Todo) VALUES(%s)", (todo,))

        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect(url_for('index'))


    return render_template('create.html', title='Create Todo', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # get form and get data from mysql db

    form = TodoForm()
    cnx = getdb_connection()
    cursor = cnx.cursor()
    # handle post request and update the todo
    if form.validate_on_submit():
        todo = form.data['todo']
        cursor.execute("UPDATE todo SET Todo = (%s) WHERE id = (%s)", (todo,id))
        cnx.commit()
        cursor.close()
        cnx.close()

        return redirect(url_for('index'))

    # handle get request for form and co
    cursor.execute("SELECT * FROM todo WHERE id = (%s)", (id,))
    # input data gotten into the form
    todo = cursor.fetchone()
    if todo:
        # assign the todo text to form to show in input
        form.todo.data = todo[1]
    else:
        form.todo.data = ''
    return render_template('edit.html', title="edit", form=form)


# for delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cnx = getdb_connection()
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM todo WHERE id = (%s)',(id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return redirect(url_for('index'))
