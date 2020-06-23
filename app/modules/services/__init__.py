# -*- coding:utf-8  -*-

import psutil
from flask import Flask


def init_services(app: Flask):
    @app.route("/cpu")
    def get_cpu() -> str:
        """
        Função para verificar o uso da cpu
        :return: retornar em porcentagem (%)
        """
        return str(psutil.cpu_percent())

    @app.route("/ram")
    def get_ram() -> str:
        """
        Função para verificar o uso da memoria ram
        :return: retornar em porcentagem (%)
        """
        return str(dict(psutil.virtual_memory()._asdict())["percent"])

    @app.route("/swap")
    def get_swap() -> str:
        """
        Função para verificar o uso da memoria swap
        :return: retornar em porcentagem (%)
        """
        return str(dict(psutil.swap_memory()._asdict())["percent"])

    @app.route("/temperatures")
    def get_temperatures() -> str:
        """
        Função para verificar a temperatura do dispositivo
        :return: retornar em C°
        """
        return "None"
        # return str(psutil.sensors_temperatures()["acpitz"][0].current)
