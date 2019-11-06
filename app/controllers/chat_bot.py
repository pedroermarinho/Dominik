# -*- coding:utf-8  -*-
import os
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import yaml

import urllib3

from chatterbot.trainers import ChatterBotCorpusTrainer

import logging
from app.controllers.key_words import Palavra_Chave
from app.controllers.commands import Comando
from app.models.functions_db import Database
from tokens.tokens import Tokens
from app.controllers.arduino_cmd import arduino_cmd
from threading import Thread


class Dominik:  # class 3
    global arduinoCmd

    def __init__(self, arduino=arduino_cmd()):
        self.Comando = Comando(arduino)

    palavra_chaves = Palavra_Chave()

    base_de_dados = Database()

    # # Enable info level logging
    logging.basicConfig(level=logging.INFO)
    DominikBot = ChatBot('DOMINIK',
                         # storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                         read_only=False,
                         # database_uri=Tokens.database
                         )  # criando um chat bot , com o nome Assitente

    CalculadoraBot = ChatBot('CalculadoraBot',
                             logic_adapters=[
                                 "chatterbot.logic.MathematicalEvaluation"
                             ]
                             # ,input_adapter="chatterbot.input.VariableInputTypeAdapter"
                             # ,output_adapter="chatterbot.output.OutputAdapter"
                             )

    trainerDominikBot = ChatterBotCorpusTrainer(DominikBot)

    print('\nOlá, Bem Vindo ao nosso bot :)\n')

    def train(self, url):  # finção para treinar o chatteot com novos aquivos
        # try:

        self.trainerDominikBot.train( "chatterbot.corpus.portuguese")
        # http = urllib3.PoolManager()
        # response = http.request('GET', str(url))
        # data = response.data.decode('utf-8')
        # yml_data = yaml.load(data)
        #
        # print(yml_data)
        # self.trainerDominikBot.train(yml_data)  # trrinar o bot com as palavras

        # except:
        #     print("Erro função-> treino")

    def mensagem_bot_pergunta(self, text=None):  # função que ira tratar as mensagens
        if text is None:  # caso a função nao recebar nenhum parametro ele ira receber o parametro do terminal
            return input('\nDigite algo:')
        else:
            return str(text)  # tranforma a variavel text em string

    result_mensagem_bot_resposta = None

    def mensagem_bot_resposta(self, cmd):  # função responsavel por gera uma reposta para a pergunta
        result = self.Comando.executar_cmd(
            self.Comando.comando(cmd))  # verifica se é um comando e se for retonara o resultado
        if result is None:  # verifica se é algum comado
            result = self.palavra_chaves.pesquisa_na_wikipedia(cmd)  # verifica se é uma pesquisa , se for <retornara o resultado da pesquisa

            if result is None:  # verifica se é algum comado
                result = self.palavra_chaves.pesquisa_definicao(
                    cmd)  # verifica se é uma pesquisa , se for <retornara o resultado da pesquisa

                if result is None:  # verifica se é algum comado
                    result = self.palavra_chaves.pesquisa_no_google(
                        cmd)  # verifica se é uma pesquisa , se for <retornara o resultado da pesquisa

                    if result is None:
                        calc = cmd.replace('Quanto é',
                                           '')  # troca calc por What is pois calculadora sor recee comandos em ingles
                        try:

                            for letras in calc:
                                if letras.isalpha():
                                    calc = None
                                    break

                            if calc is not None:
                                result = self.CalculadoraBot.get_response(calc)  # função da chamda da calculadora
                                if result.confidence < 0.99:  # se a confiança da calcualdora for aixa ele retorna none
                                    result = None
                                elif result == "e = 2.718281":
                                    result = None
                            else:
                                result = None

                        except:  # se der errp
                            result = None

                        if result is None:
                            result = self.DominikBot.get_response(
                                cmd)  # mostra a resposta do bot de acordo com banco de dado

                            print(result.confidence)
                            print(result)
                            confiaca = result.confidence  # mostra o tao confiante a resposta é
                            if result.confidence <= 0.70:
                                try:
                                    Thread(target=self.base_de_dados.add_new_word,
                                           args=(cmd,)).start()  # grava nova palavra no banco de dado
                                    # self.base_de_dados.add_nova_palavra(cmd)  # grava nova palavra no banco de dado
                                except:
                                    print('\nErro: palavras\n')

                            if result.confidence <= 0.50:
                                resposta = result
                                print('\nErro: confiança menor que 0.:60', result, '\n')
                                result = self.palavra_chaves.wikipedia(cmd)  # retorna uma pesquisa da wikipedia

                                if result is None:
                                    result = 'Infelizmente não sei responder\nMas eu tenho ' + str(
                                        int(confiaca * 100)) + '% de confiança que a reposta correta é: \n' + str(
                                        resposta)
        return result  # retorna ao resultado


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # print(yaml.load_all("https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/conversations.yml"))

    main = Dominik()
    # main.train("https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/conversations.yml")
    while True:
        print(main.mensagem_bot_resposta(main.mensagem_bot_pergunta()))
