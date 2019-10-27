# -*- coding:utf-8  -*-
import os
from chatterbot import ChatBot
import shutil

import logging
from Palavras_Chave import Palavra_Chave
from Comandos import Comando
from BD import banco_de_dados
from tokens.tokens import Tokens
from Arduino_CMD import arduino_cmd
from threading import Thread

class Main:  # class 3
    global arduinoCmd

    def __init__(self, arduino=arduino_cmd()):
        self.Comando = Comando(arduino)

    palavra_chaves = Palavra_Chave()


    base_de_dados = banco_de_dados()

    # # Enable info level logging
    logging.basicConfig(level=logging.INFO)
    DominikBot = ChatBot('DOMINIK',
                         storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                         read_only=False,
                         database_uri=Tokens.database
                         )  # criando um chat bot , com o nome Assitente

    CalculadoraBot = ChatBot('CalculadoraBot',
                             logic_adapters=[
                                 "chatterbot.logic.MathematicalEvaluation"
                             ]
                             # ,input_adapter="chatterbot.input.VariableInputTypeAdapter"
                             # ,output_adapter="chatterbot.output.OutputAdapter"
                             )

    # Emojibot = ChatBot('EmojiBot')

    print('\nOlá, Bem Vindo ao nosso bot :)\n')

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
            result = self.palavra_chaves.pesquisa_na_wikipedia(
                cmd)  # verifica se é uma pesquisa , se for <retornara o resultado da pesquisa

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
                                    Thread(target=self.base_de_dados.add_nova_palavra,args=(cmd,)).start()# grava nova palavra no banco de dado
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
    main = Main()
    while True:
        main.mensagem_bot_pergunta()
