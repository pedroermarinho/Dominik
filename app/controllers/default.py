from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from app import app, db, login_manager

from app.models.forms import LoginForm, RegisterForm, In_formallyForm

from app.models.tables import User

from app.controllers.chat_bot import Dominik
from app.controllers.file import download_yml

import urllib3
import json

bot_dominik = Dominik()


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


@app.errorhandler(404)
@app.route('/404')
def not_found(e=None):
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


@app.route('/register', methods=["POST", "GET"])
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
            i = User(str(register_form.username.data), str(register_form.password.data), str(register_form.name.data),
                     str(register_form.email.data))
            db.session.add(i)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', register_form=register_form)


@app.route('/tables_dic', methods=['GET', 'POST'])
def tables_dic():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        form_dic_type = In_formallyForm()
        http = urllib3.PoolManager()
        response = http.request('GET', "https://pedroermarinho.github.io/Dominik-dic/src/yml/formally.json")
        if form_dic_type.validate_on_submit():
            value = form_dic_type.type_dic_radio.data
            if value == 'formally':
                response = http.request('GET', "https://pedroermarinho.github.io/Dominik-dic/src/yml/formally.json")
                flash('Formally')
            elif value == 'informally':
                response = http.request('GET', "https://pedroermarinho.github.io/Dominik-dic/src/yml/informally.json")
                flash('Informally')
        else:
            flash(str(form_dic_type.errors))

        print(request.method)
        if request.method == 'POST':
            print("request.form=>>>>>" + str(request.form))
            if "Download" in request.form:
                print(request.form.get('Download'))
            elif "Update" in request.form:
                print(request.form.get('Update'))
            elif "Delete" in request.form:
                print(request.form.get('Delete'))

        link_dada = json.loads(response.data.decode('utf-8'))
        return render_template('tables_dic.html', link_dada=link_dada, form_dic_type=form_dic_type)


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


# define app routes
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route('/test')
def test():
    return render_template('test.html')


@app.route("/get")
def get_bot_response():
    download_dic = request.args.get('download_dic')
    update_dic = request.args.get('update_dic')
    delete_dic = request.args.get('delete_dic')
    userText = request.args.get('msg')
    test = request.args.get('test')
    print(test)
    if userText is not None:
        print(userText)
        return str(bot_dominik.mensagem_bot_resposta(bot_dominik.mensagem_bot_pergunta(userText)))
    elif download_dic is not None:
        print("download_dic")
        download_dic = download_dic.replace("\'", "\"")
        download_dic = json.loads(download_dic)
        download_yml(download_dic["url"], download_dic["subcategory"])
        flash("Download do Arquivo "+download_dic["subcategory"]+" Concluído com Sucesso")
        return ""
    elif update_dic is not None:
        print("update_dic")
        update_dic = update_dic.replace("\'", "\"")
        update_dic = json.loads(update_dic)
        print(update_dic)
        return ""
    elif delete_dic is not None:
        print("delete_dic")
        delete_dic = delete_dic.replace("\'", "\"")
        delete_dic = json.loads(delete_dic)
        print(delete_dic)
        # data = json.load(delete_dic)
        # print(data)
        return ""
    else:
        return None
