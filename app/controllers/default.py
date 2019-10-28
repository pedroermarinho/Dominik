from flask import render_template
from app import app


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/404')
def er404():
    return render_template('404.html')


@app.route('/forgot-password')
def forgotpassword():
    return render_template('forgot-password.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')



