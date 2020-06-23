# -*- coding:utf-8  -*-

import json

import urllib3
from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from app.models.forms import In_formallyForm
from app.modules.chat_bot.controller import bot_dominik
from app.controllers import filer
from app.controllers.filer import list_file_yml_dic
from app.controllers.filer import download_yml, delete_yml


def init_chat_bot(app: Flask):
    @app.route('/tables_dic', methods=['GET', 'POST'])
    def tables_dic():
        """
        Página de tabelas com os dicionarios disponiveis
        :return:
        """
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
                    response = http.request('GET',
                                            "https://pedroermarinho.github.io/Dominik-dic/src/yml/informally.json")
                    flash('Informally')
            else:
                pass
                # flash(str(form_dic_type.errors))

            link_dada = json.loads(response.data.decode('utf-8'))
            return render_template('tables_dic.html', link_dada=link_dada, form_dic_type=form_dic_type, filer=filer)

    @app.route("/train")
    def train():
        """
        Página para fazer o treinamento do chatbot
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            Train_dic = request.args.get('Train_dic')
            if Train_dic is not None:
                bot_dominik.train(Train_dic)
                flash("Treino Concluido ")
            return render_template("train.html", list_dic=list_file_yml_dic())

    @app.route("/chatbot")
    def chatbot():
        """
        Página com um terminal para teste com chatbot
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template("chatbot.html")

    @app.route("/chatbot/get")
    def chat_bot_response():
        userText = request.args.get('msg')
        if userText is not None:
            print(userText)
            return str(bot_dominik.mensagem_bot_resposta(bot_dominik.mensagem_bot_pergunta(userText)))
            pass

    @app.route("/train/download")
    def train_download_response():
        download_dic = request.args.get('download_dic')
        if download_dic is not None:
            # print("download_dic")

            download_dic = download_dic.replace("\'", "\"")
            download_dic = json.loads(download_dic)
            download_yml(download_dic["url"], download_dic["subcategory"])
            flash("Download do arquivo " + download_dic["subcategory"] + " concluído com sucesso")
            return ""

    @app.route("/train/update")
    def train_update_response():
        update_dic = request.args.get('update_dic')
        if update_dic is not None:
            update_dic = update_dic.replace("\'", "\"")
            update_dic = json.loads(update_dic)
            download_yml(update_dic["url"], update_dic["subcategory"])
            flash("Atualização do arquivo " + update_dic["subcategory"] + " concluído com sucesso")
            return ""

    @app.route("/train/delete")
    def train_delete_response():
        delete_dic = request.args.get('delete_dic')
        if delete_dic is not None:
            # print("delete_dic")
            delete_dic = delete_dic.replace("\'", "\"")
            delete_dic = json.loads(delete_dic)
            delete_yml(delete_dic["url"], delete_dic["subcategory"])
            flash("Arquivo " + delete_dic["subcategory"] + " deletado com sucesso")
            return ""
