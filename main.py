import sqlite3
import os
from flask import Flask, render_template, request, flash, url_for, abort, session, redirect
from database import DataBase

DATABASE = 'tmp/flsk.db'
DEBUG = True
SECRET_KEY = 'My_key_1'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({'DATABASE': os.path.join(app.root_path, 'flsk.db')})

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con

def create_db():
    db = connect_db()
    with open('create_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# menu = [{'name': 'Главная', 'url': 'index'},
#         {'name': 'О нас', 'url': 'about'},
#         {'name': 'Услуги', 'url': 'services'},
#         {'name': 'Наши врачи', 'url': 'doctors'},
#         {'name': 'Контакты', 'url': 'contacts'},
#         ]


@app.route('/index')
@app.route('/')
def index():
    db = connect_db()
    dbase = DataBase(db)
    return render_template('index.html', title='Главная',
                           menu=dbase.get_objects('mainmenu'),
                           posts=dbase.get_objects('posts'))


@app.route('/about')
def about():
    db = connect_db()
    dbase = DataBase(db)
    return render_template('about.html', title='О нас', menu=dbase.get_objects('mainmenu'))


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    db = connect_db()
    dbase = DataBase(db)

    if request.method == 'POST':
        if 'username' in request.form:
            if len(request.form['username']) > 1:
                flash('Сообщение отправлено успешно!', category='success')
            else:
                flash('Ошибка отправки', category='error')

            context = {
                'username': request.form['username'],
                'email': request.form['email'],
                'message': request.form['message'],
            }
            return render_template('contacts.html', title='Контакты', menu=dbase.get_objects('mainmenu'), **context,
                                   posts=dbase.get_objects('posts'))

        elif 'title' in request.form:
            if len(request.form['title']) < 3 or len(request.form['text']) < 1:
                flash('Ошибка добавления отзыва', category='error')
            else:
                res = dbase.add_post(request.form['title'], request.form['text'], request.form['url'])
                if res:
                    flash('Отзыв добавлен успешно!', category='success')
                else:
                    flash('Ошибка добавления отзыва', category='error')

    return render_template('contacts.html', title='Контакты', menu=dbase.get_objects('mainmenu'),
                           posts=dbase.get_objects('posts'))


@app.route('/post/<post_id>')
def show_post(post_id):
    db = connect_db()
    dbase = DataBase(db)

    title, post = dbase.get_post(post_id)
    if not title:
        abort(404)

    return render_template('post.html', title=title, post=post, menu=dbase.get_objects('mainmenu'))



@app.route('/services')
def services():
    db = connect_db()
    dbase = DataBase(db)
    return render_template('services.html', title='Уcлуги', menu=dbase.get_objects('mainmenu'))


@app.route('/doctors')
def doctors():
    db = connect_db()
    dbase = DataBase(db)
    return render_template('doctors.html', title='Наши врачи', menu=dbase.get_objects('mainmenu'))

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'Пользователь {username}'

@app.route('/login', methods=['GET','POST'])
def login():
    db = connect_db()
    dbase = DataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' \
                                  and request.form['password'] == 'qwerty':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=dbase.get_objects('mainmenu'))

@app.errorhandler(404)
def page_not_found(error):
    db = connect_db()
    dbase = DataBase(db)
    return render_template('page404.html', title='Cтраница не найдена', menu=dbase.get_objects('mainmenu'))

if __name__ == '__main__':
    create_db()
    app.run()