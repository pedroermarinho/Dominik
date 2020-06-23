# -*- coding:utf-8  -*-
import logging

from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from app.controllers.database import db, login_manager
from app.models.forms import LoginForm, RegisterForm, TelegramForm, DataBaseForm
from app.modules.chat_bot.controller import chat_bot
from app.models.tables import User, TelegramToken, DataBase


def init_app(app: Flask):
    logging.warning(__name__)

    global bot_dominik
    bot_dominik = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @app.route('/home')
    @app.route('/index')
    @app.route('/')
    def home():
        """
        Página principal
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('index.html')

    @app.route('/about')
    def about():
        """
        Página de informações
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('about.html')

    @app.route('/blank')
    def blank():
        """
        Página sem nada
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('blank.html')

    @app.route('/charts')
    def charts():
        """
        Página de exemplos de graficos
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('charts.html')

    @app.errorhandler(404)
    @app.route('/404')
    def not_found(e=None):
        """
        Página de erro
        :param e:
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('404.html')

    @app.route('/forgot-password')
    def forgotpassword():
        """
        Página para recuperar a senha
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('forgot-password.html')

    @app.route('/login', methods=["POST", "GET"])
    def login():
        """
        Página de login
        :return:
        """
        login_form = LoginForm()
        if User.query.count() == 0:
            return redirect(url_for("register"))
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
    # @login_required
    def register():
        """
        Página para regitrar novos usuarios
        :return:
        """
        register_form = RegisterForm()
        if register_form.validate_on_submit():
            user = User.query.filter_by(username=register_form.username.data).first()
            email = User.query.filter_by(email=register_form.email.data).first()
            if user:
                flash("Usuário inválido")
            elif email:
                flash("Email inválido")
            else:
                i = User(
                    str(register_form.username.data),
                    str(register_form.password.data),
                    str(register_form.name.data),
                    str(register_form.email.data)
                )
                db.session.add(i)
                db.session.commit()
                return redirect(url_for('login'))

        return render_template('register.html', register_form=register_form)

    @app.route('/base')
    def base():
        """
        Página base para toda a contrução das outras paginas
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('base.html')

    @app.route('/logout')
    def logout():
        """
        função para sair do sistema(logout)
        :return:
        """
        logout_user()
        flash("Logger out.")
        return redirect(url_for('login'))

    @app.route("/settings")
    @login_required
    def settings():
        """
        Página para o menu de configuração
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template("settings.html")

    @app.route("/database", methods=["POST", "GET"])
    def database():
        """
        Página para configurar os bancos de dados
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            dataBaseForm = DataBaseForm()
            if dataBaseForm.validate_on_submit():
                database_url = DataBase.query.filter_by(database_url=str(
                    'mysql+pymysql://' + str(dataBaseForm.user.data) + ':@' + str(
                        dataBaseForm.password.data) + '@' + str(
                        dataBaseForm.host.data) + '/' + str(dataBaseForm.database.data))).first()
                if database_url:
                    flash("Dados inválidos")
                else:
                    i = DataBase(
                        str(dataBaseForm.host.data),
                        str(dataBaseForm.database.data),
                        str(dataBaseForm.user.data),
                        str(dataBaseForm.password.data)
                    )
                    db.session.add(i)
                    db.session.commit()
                    return redirect(url_for('database'))

            return render_template('database.html', dataBaseForm=dataBaseForm, dataBase=DataBase.query.all())

    @app.route("/telegram", methods=["POST", "GET"])
    def telegram():
        """
        Página para fazer a configuração da interface de cominicação com o telegram
        :return:
        """
        telegramForm = TelegramForm()
        if telegramForm.validate_on_submit():
            name = TelegramToken.query.filter_by(name=telegramForm.name.data).first()
            token = TelegramToken.query.filter_by(token=telegramForm.token.data).first()
            if name:
                flash("Nome inválido")
            elif token:
                flash("Token inválido")
            else:
                i = TelegramToken(
                    str(telegramForm.name.data),
                    str(telegramForm.token.data)
                )
                db.session.add(i)
                db.session.commit()
                return redirect(url_for('telegram'))

        return render_template('telegram.html', telegramForm=telegramForm, telegramData=TelegramToken.query.all())

    @app.route("/users", methods=["POST", "GET"])
    def users():
        """
        Página para gerenciar os usuarios
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template("users.html")

    @app.route("/whatsapp", methods=["POST", "GET"])
    def whatsapp():
        """
        Página para fazer a configuração da interface de cominicação com o whatsapp
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template("whatsapp.html")

    @app.route('/test')
    def test():
        """
        Página de teste
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template('test.html')

    @app.route("/get")
    def get_bot_response():
        """
        Função que reposavel por fazer algumas operações
        :return:
        """


        test = request.args.get('test')
        print(test)

        #
        # else:
        #     return None
