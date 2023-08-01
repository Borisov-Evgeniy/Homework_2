from flask import Flask, render_template

app = Flask(__name__)

menu = [{'name': 'Главная','url': 'index'},
        {'name': 'О нас', 'url': 'about'},
        {'name': 'Услуги', 'url': 'services'},
        {'name': 'Наши врачи', 'url': 'doctors'},
        {'name': 'Контакты', 'url': 'contacts'},
        ]

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='Главная', menu=menu)

@app.route('/about')
def about():
    return render_template('about.html', title='О нас', menu=menu)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакты', menu=menu)

@app.route('/services')
def services():
    return render_template('services.html', title='Уcлуги', menu=menu)

@app.route('/doctors')
def doctors():
    return render_template('doctors.html', title='Наши врачи', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)