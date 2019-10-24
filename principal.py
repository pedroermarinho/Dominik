# -*- coding:utf-8  -*-
import os
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import shutil
from chatterbot.trainers import ChatterBotCorpusTrainer

import logging
from assbot.Palavras_Chave import Palavra_Chave
from assbot.Comandos import Comando
from assbot.dados_sql.BD import banco_de_dados

class Main(object):  # class 3
    palavra_chaves = Palavra_Chave()
    Comando = Comando()
    base_de_dados = banco_de_dados()

    base_de_dados.add_curiosidade()
    base_de_dados.add_piadas()
    base_de_dados.add_quiz()

    # Enable info level logging
    logging.basicConfig(level=logging.INFO)
    DominikBot = ChatBot('DOMINIK',
                  storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                  database_uri='mongodb://localhost:27017/DOMINIK'
                  )  # criando um chat bot , com o nome Assitente

    CalculadoraBot = ChatBot('CalculadoraBot',
                             logic_adapters=[
                                 "chatterbot.logic.MathematicalEvaluation"
                             ],
                             input_adapter="chatterbot.input.VariableInputTypeAdapter",
                             output_adapter="chatterbot.output.OutputAdapter")

    trainerDominikBot = ChatterBotCorpusTrainer(DominikBot)

    
    Emojibot = ChatBot('EmojiBot')
    trainerEmoji = ChatterBotCorpusTrainer(Emojibot)
   
    

    print('\nOlá, Bem Vindo ao nosso bot :)\n')

    def treino(self):  # finção para treinar o chatteot com novos aquivos
        print("treino")
        # self.treinoEmoji()
        try:
            for _arquivo in os.listdir('assbot/chats_yml'):  # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".yml"):
                    print(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    self.trainerDominikBot.train('assbot/chats_yml/' + _arquivo)  # trrinar o bot com as palavras
                    shutil.move('assbot/chats_yml/' + _arquivo,
                                'assbot/chats_ja_treinados/')  # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
        except:
            print("Erro função-> treino")


    def treinoEmoji(self):  # finção para treinar o chatteot com novos aquivos
        print("treinoEmoji")
        try:
            for _arquivo in os.listdir('assbot/chats_Emoji'):  # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".txt"):
                    print(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    linhas = open('assbot/chats_Emoji/' + _arquivo, 'r').readlines()  # vamos ler linhas
    
                    self.trainerEmoji.train(linhas)  # trrinar o bot com as palavras
    
                    shutil.move('assbot/chats_Emoji/' + _arquivo,
                                'assbot/chats_Emoji_ja_treinados/')  # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
        except:
            print("Erro função-> treino")

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
                            result = self.DominikBot.get_response(cmd)  # mostra a resposta do bot de acordo com banco de dado
                            print(result.confidence)
                            confiaca = result.confidence  # motra o tao confiante a resposta é
                            if result.confidence <= 0.85:
                                try:
                                    arq = open('assbot/palavras_6/palavras.txt', 'a')
                                    arq.writelines('\n\n' + str(cmd))  # gravar palavras desconhecida
                                    arq.close()
                                except:
                                    print('\nErro: palavras\n')

                            if result.confidence <= 0.0:
                                resposta = result
                                print('\nErro: confiança menor que 0.:60', result, '\n')
                                result = self.palavra_chaves.wikipedia(cmd)

                                if result is None:
                                    result = 'Infelizmente não sei responder\nMas eu tenho ' + str(
                                        int(confiaca * 100)) + '% de confiança que a reposta correta é: \n' + str(
                                        resposta)
        return result  # retorna ao resultado

# ----------------------------------------------------------------------------------------------------------------------
