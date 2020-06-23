# -*- coding:utf-8  -*-

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask


def init_arduino(app: Flask):
    @app.route("/hardware")
    def hardware():
        """
        Página para a configuração do hardware
        :return:
        """
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        else:
            return render_template("hardware.html")

