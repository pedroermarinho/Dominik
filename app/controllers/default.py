from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import app, db, login_manager

from app.models.forms import LoginForm , RegisterForm


from app.models.tables import User



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('about.html')


@app.route('/blank')
def blank():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('blank.html')


@app.route('/charts')
def charts():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('charts.html')


@app.route('/404')
def er404():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('404.html')


@app.route('/forgot-password')
def forgotpassword():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('forgot-password.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password == login_form.password.data:
            login_user(user)
            flash("Logger in")
            return redirect(url_for("home"))
        else:
            flash("Invalid login")

    return render_template('login.html', login_form=login_form)


@app.route('/register',methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User.query.filter_by(username=register_form.username.data).first()
        email = User.query.filter_by(email=register_form.email.data).first()
        if user:
            flash("Usuário inválido")
        elif email:
            flash("Email inválido")
        else:
            i = User(str(register_form.username.data), str(register_form.password.data), str(register_form.name.data), str(register_form.email.data))
            db.session.add(i)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('register.html', register_form=register_form)


@app.route('/tables')
def tables():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('tables.html')


@app.route('/base')
def base():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('base.html')


@app.route('/logout')
def logout():
    logout_user()
    flash("Logger out.")
    return redirect(url_for('login'))


@app.route("/settings")
@login_required
def settings():
    pass


@app.route('/test/<info>')
@app.route('/test/', defaults={'info': None})
def test(info):
    i = User("pedro123", "1234", "pedro", "pedro.marinho2348")
    db.session.add(i)
    db.session.commit()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('test.html', info="ok")


from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

portugueseBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(portugueseBot)
# trainer.train("chatterbot.corpus.portuguese") #train the chatter bot for english

#define app routes
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(portugueseBot.get_response(userText))




