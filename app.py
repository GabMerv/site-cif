import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory
from werkzeug.exceptions import abort
import os

global adminToken
adminToken = 'wpoLlkQ7h4Mz5aVnpiA4'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jesuisunebicorne'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        name = request.form['name']
        mail = request.form['mail']
        reponse = request.form['response']
        responseWriter = request.form['responseWriter']

        if not title:
            flash('Vous devez ajouter un titre')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, details = ?, name = ?, mail = ?, response = ?, responseWriter = ?'
                         ' WHERE id = ?',
                         (title, details, name, mail, reponse, responseWriter, id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin', administrateur=adminToken))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin', administrateur=adminToken))


@app.route('/connection', methods=('GET', 'POST'))
def connection():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    clean_users = []
    for user in users:
        temp_user = [user['name'], user['psw']]
        clean_users.append(temp_user)
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        for user in clean_users:
            if userName == user[0]:
                password = "".join(str(ord(char)) for char in password)
                if password == user[1]:
                    return redirect(url_for('admin', administrateur=adminToken))
                else:
                    return redirect(url_for('index'))
    return render_template('index.html', users=True)

@app.route('/admin/<administrateur>', methods=('GET', 'POST'))
def admin(administrateur=False):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        name = request.form['name']
        mail = request.form['mail']

        if title and mail and name:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, details, name, mail) VALUES (?, ?, ?, ?)',
                             (title, details, name, mail))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        if not title:
            flash("Vous devez ajouter un titre")
        if not mail:
            flash("Vous devez renseigner un mail")
        if not name:
            flash('Vous devez renseigner un nom')

    return render_template('admin.html', posts=posts, admin=administrateur)

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        name = request.form['name']
        mail = request.form['mail']

        if title and mail and name:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, details, name, mail) VALUES (?, ?, ?, ?)',
                             (title, details, name, mail))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        if not title:
            flash("Vous devez ajouter un titre")
        if not mail:
            flash("Vous devez renseigner un mail")
        if not name:
            flash('Vous devez renseigner un nom')

    return render_template('index.html', posts=posts, users=None)

if __name__ == "__main__":
    app.run(threaded=True, debug=False, host='0.0.0.0')