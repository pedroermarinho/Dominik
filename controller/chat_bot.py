# -*- coding:utf-8  -*-
from chatterbot import ChatBot
from config import DATABASE_URI_CHAT_DEFAULT

from chatterbot.trainers import ChatterBotCorpusTrainer

import logging
from controller import key_words
from controller import commands
from controller import functions_db
from controller import arduinocmd
from threading import Thread


class Dominik:  # class 3
    logging.warning(__name__)

    def __init__(self):
        print(str(__name__) + '__init__')
        self.Comando = commands.Comando(arduinocmd.ArduinoCMD())
        self.base_de_dados = functions_db.Database()
        self.palavra_chaves = key_words.PalavraChave()


        self.DominikBot = ChatBot('DOMINIK',
                                  # storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                                  read_only=False,
                                  # database_uri=Tokens.database
                                  database_uri=DATABASE_URI_CHAT_DEFAULT
                                  )  # criando um chat bot , com o nome Assitente
        self.CalculadoraBot = ChatBot('CalculadoraBot',
                                      logic_adapters=[
                                          "chatterbot.logic.MathematicalEvaluation"
                                      ]
                                      # ,input_adapter="chatterbot.input.VariableInputTypeAdapter"
                                      # ,output_adapter="chatterbot.output.OutputAdapter"
                                      )

        self.trainerDominikBot = ChatterBotCorpusTrainer(self.DominikBot)

    logging.warning(str(__name__) + ':Olá, Bem Vindo ao nosso bot :)')

    def train(self, url):  # finção para treinar o chatteot com novos aquivos
        try:

            self.trainerDominikBot.train(url)

        except:
            print(str(__name__) + ":Erro função-> treino")

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

                            logging.warning(str(__name__) + ':'+str(result.confidence))
                            logging.warning(str(__name__) + ':'+str(result))
                            confiaca = result.confidence  # mostra o tao confiante a resposta é
                            if result.confidence <= 0.70:
                                try:
                                    Thread(target=self.base_de_dados.add_new_word,
                                           args=(cmd,)).start()  # grava nova palavra no banco de dado
                                    # self.base_de_dados.add_nova_palavra(cmd)  # grava nova palavra no banco de dado
                                except:
                                    logging.warning(str(__name__) + ':Erro: palavras')

                            if result.confidence <= 0.50:
                                resposta = result
                                logging.warning(str(__name__) + ':Erro: confiança menor que 0.:60 ->'+ str(result))
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
