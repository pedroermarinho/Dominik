# -*- coding:utf-8  -*-
import logging
import pymysql
import random
from model.question import quest
from tokens.tokens import Tokens
import shutil
import os


class Database:

    logging.warning(__name__)

    def __init__(self):

        print(str(__name__) + '__init__')
        self.keywords_wikipedia = []  # palavras chaves para pesquisas na wikipedia
        self.keywords_google = []  # palavras chaves para pesquisas no google
        self.definition_words = []  # palavras chaves para pesquisas no dicionario
        self.dic_cmd = {}  # criando um dicionario comandos
        self.dic_message_cmd = {}  # criando um dicionario comandos de menagem
        self.connection = None
        self.cursor = None
        self.connection_on()

    def connection_on(self):
        """


        :return:
        """

        try:
            # Abrimos uma conexão com o banco de dados:
            self.connection = pymysql.connect(host=Tokens.host, db=Tokens.db, user=Tokens.user,
                                              passwd=Tokens.passwd)
            # Cria um cursor:
            self.cursor = self.connection.cursor()
        except pymysql.err.OperationalError as e:
            logging.error(str(__name__) + ":erro conexão banco de dados:"+str(e))
            self.connection = None
            self.cursor = None

    def add_base_de_users(self, _id: int, nome: str):
        """

        :param _id: ID do usuario
        :param nome: Nome do usuario
        :return:
        """
        logging.warning("add_base_de_usuarios")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO base_de_usuarios VALUES (\'" + str(_id) + "\',\'" + str(
                    nome) + "\')")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.

            except Exception as e:
                logging.error(str(__name__) + ":Erro função-> add_base_de_usuarios:"+str(e))
                self.connection_on()
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def add_new_word(self, text: str):
        logging.warning("add_nova_palavra")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO `novas_palavras`(`texto`) VALUES (\'" + str(
                    text) + "\')")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.

            except Exception as e:
                logging.error(str(__name__) + ":Erro função-> add_nova_palavra:"+str(e))
                self.connection_on()
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def add_positive_point(self, _id: int, last_question):
        """
        Adiciona pontos positivos
        :param _id: ID do usuario
        :param last_question: ultima pergunta
        :return:
        """
        logging.warning("add_positive_point")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO usuario  VALUES (\'" + str(_id) + "\',\'" + str(2) + "\'," + str(
                    last_question) + ")")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.
            except Exception as e:
                try:
                    ultima_pergunta_banco = self.get_last_question(_id)

                    logging.warning(str(ultima_pergunta_banco) + "==" + str(last_question))

                    if ultima_pergunta_banco != last_question:
                        self.cursor.execute("UPDATE usuario SET pontuacao = (pontuacao + 2) WHERE id =\'" + str(
                            _id) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.
                        self.cursor.execute(
                            "UPDATE usuario SET ultima_pergunta = " + str(last_question) + " WHERE id =\'" + str(
                                _id) + "\'")
                        self.connection.commit()  # Efetua um commit no banco de dados.

                except Exception as e:
                    logging.error(str(__name__) + ":Erro função-> add_pontucao_acetou:"+str(e))
                    self.connection_on()
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def add_negative_point(self, _id: int, last_question):
        """
        Adiciona pontos negativos
        :param _id: ID do usuario
        :param last_question: ultima pergunta
        :return:
        """
        logging.warning("add_pontucao_errou id =" + str(_id) + " ultima_pergunta =" + str(last_question))

        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO usuario  VALUES (\'" + str(_id) + "\',\'" + str(-1) + "\'," + str(
                    last_question) + ")")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.
            except Exception as e:

                try:
                    ultima_pergunta_banco = self.get_last_question(_id)

                    logging.warning(str(ultima_pergunta_banco) + "==" + str(last_question))

                    if ultima_pergunta_banco != last_question:
                        self.cursor.execute("UPDATE usuario SET pontuacao = (pontuacao - 1)   WHERE id =\'" + str(
                            _id) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.
                        self.cursor.execute(
                            "UPDATE usuario SET ultima_pergunta = (" + str(last_question) + ") WHERE id =\'" + str(
                                _id) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.

                except Exception as e:
                    logging.error(str(__name__) + ":Erro função-> add_pontucao_errou:"+str(e))
                    self.connection_on()
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def get_last_question(self, _id: int):
        """

        :param _id: ID do usuario
        :return:
        """
        logging.warning("get_ultima_resposta")
        if self.connection is not None:
            try:
                self.connection.commit()  # Efetua um commit no banco de dados.
                self.cursor.execute("SELECT ultima_pergunta FROM usuario WHERE id = \'" + str(_id) + "\'")

                results = self.cursor.fetchall()
                logging.warning(results)
                result = None
                for res in results:
                    for resposta in res:
                        result = resposta

                logging.warning(result)
                return result
            except Exception as e:
                logging.error(str(__name__) + ":Erro função-> get_ultima_resposta:"+str(e))
                self.connection_on()
                return 0
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def get_point(self, _id: int):
        """

        :param _id: ID do usuario
        :return:
        """
        logging.warning("get_pontuacao")
        if self.connection is not None:
            try:
                self.cursor.execute("SELECT pontuacao FROM usuario WHERE id = \'" + str(_id) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(resposta)

                logging.warning(result)
                return result
            except Exception as e:
                logging.error(str(__name__) + ":Erro função-> get_pontuacao:"+str(e))
                self.connection_on()
                return 0
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def add_curiosidade(self):
        logging.warning("add_curiosidade")
        if self.connection is not None:
            # try:
            for _arquivo in os.listdir('assbot/ass_diversos/curiosidade'):
    # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".txt"):
                    logging.warning(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    linhas = open('assbot/ass_diversos/curiosidade/' + _arquivo, 'r').readlines()  # vamos ler linhas
                    for linha in linhas:
                        linha = linha.replace('\n', '')
                        self.cursor.execute("INSERT INTO curiosidades (curiosidade) VALUES (\'" + str(
                            linha) + "\')")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.

                    shutil.move('assbot/ass_diversos/curiosidade/' + _arquivo,
                                'assbot/ass_diversos/curiosidade/ja_treinados/')
                    # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
            # except:
            #     logging.error(str(__name__)+":Erro função-> treino curiosidade")
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def add_quiz(self):
        logging.warning("add_quiz")
        if self.connection is not None:
            # try:
            for _arquivo in os.listdir('assbot/quiz'):  # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".txt"):
                    logging.warning(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    arquivo = open('assbot/quiz/' + _arquivo, 'r').readlines()
                    for comando in arquivo:  # percorendo todos os comandos
                        comando = comando.replace('\n', '')  # deletando as quebras de linha
                        parts = comando.split('||')  # separando mensaguem de comando // dicionario de comandos
                        self.cursor.execute(
                            "INSERT INTO quiz (pergunta, alternativa1, alternativa2, alternativa3, alternativa4, "
                            "alternativa5, resposta) VALUES (\'" + str(
                                parts[0]) + "\',\'" + str(parts[1]) + "\',\'" + str(parts[2]) + "\',\'" + str(
                                parts[3]) + "\',\'" + str(parts[4]) + "\',\'" + str(parts[5]) + "\',\'" + str(
                                parts[6]) + "\')")
                        self.connection.commit()  # Efetua um commit no banco de dados.
                    shutil.move('assbot/quiz/' + _arquivo,
                                'assbot/quiz/ja_treinados/')
                    # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
            # except:
            #     logging.error(str(__name__)+":Erro função-> treino quiz")
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")

    def Numero_aleatorio_piada(self):
        """


        :return:
        """
        logging.warning("Numero_aleatorio_piada")
        if self.connection is not None:
            try:
                self.cursor.execute("SELECT COUNT(*) FROM piadas")
                conts = self.cursor.fetchall()

                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except Exception as e:
                logging.error(str(__name__) + ":erro numero aleatorio piada:"+str(e))
                self.connection_on()
                return int(0)
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def Numero_aleatorio_quiz(self):
        """

        :return:
        """
        logging.warning("Numero_aleatorio_quiz")
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM quiz")
                conts = self.cursor.fetchall()
                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except Exception as e:
                logging.error(str(__name__) + ":erro numero aleatorio quiz:"+str(e))
                self.connection_on()
                return int(1)
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def Numero_aleatorio_curiosidade(self):
        """

        :return:
        """
        logging.warning("Numero_aleatorio_curiosidade")
        if self.connection is not None:
            try:
                self.cursor.execute("SELECT COUNT(*) FROM curiosidades")
                conts = self.cursor.fetchall()
                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except Exception as e:
                logging.error(str(__name__) + ":erro numero aleatorio curiosidade:"+str(e))
                self.connection_on()
                return int(0)
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_piada(self, cod: int):
        """

        :param cod:
        :return:
        """
        logging.warning("get_piada")
        if cod is None:
            cod = self.Numero_aleatorio_piada()
        logging.warning(cod)
        if self.connection is not None:
            try:
                self.cursor.execute("SELECT piada FROM piadas WHERE id = \'" + str(cod) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(cod) + ")" + str(resposta)

                return result
            except Exception as e:
                logging.error(str(__name__) + ":erro get_piada:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_curiosidade(self, cod: int):
        """

        :param cod:
        :return:
        """
        logging.warning("get_curiosidade")
        if cod is None:
            cod = self.Numero_aleatorio_curiosidade()
        if self.connection is not None:
            try:
                self.cursor.execute("SELECT curiosidade FROM curiosidades WHERE id = \'" + str(cod) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(cod) + ")" + str(resposta)
                return result
            except Exception as e:
                logging.error(str(__name__) + ":erro get_quiz:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_definicao(self):
        """

        :return:
        """
        logging.warning("get_definicao")

        if self.connection is not None:
            try:
                self.cursor.execute("SELECT texto FROM definicao")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.definition_words.insert(n, resposta)
                        n = n + 1
                return self.definition_words
            except Exception as e:
                logging.error(str(__name__) + ":erro get_definicao:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_google(self):
        logging.warning("get_google")

        if self.connection is not None:
            try:
                self.cursor.execute("SELECT texto FROM google")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.keywords_google.insert(n, resposta)
                        n = n + 1
                return self.keywords_google
            except Exception as e:
                logging.error(str(__name__) + ":erro get_google:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_wikipedia(self):
        """

        :return:
        """
        logging.warning("get_wikipedia")

        if self.connection is not None:
            try:
                self.cursor.execute("SELECT texto FROM wikipedia")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.keywords_wikipedia.insert(n, resposta)
                        n = n + 1
                return self.keywords_wikipedia
            except Exception as e:
                logging.error(str(__name__) + ":erro get_wikipedia:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None


    def get_cmds(self):
        """

        :return:
        """
        logging.warning("get_cmds")

        if self.connection is not None:
            try:
                self.cursor.execute("SELECT texto , cmd FROM cmds")

                results = self.cursor.fetchall()

                for parts in results:
                    self.dic_cmd.update(
                        {parts[0]: parts[1]})  # colocados dentro da lista as mensagens e os comandos
                return self.dic_cmd
            except Exception as e:
                logging.error(str(__name__) + ":erro get_cmds:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_mensagem_cmd(self):
        """

        :return:
        """
        logging.warning("get_cmds")

        if self.connection is not None:
            try:
                self.cursor.execute("SELECT cmd , texto  FROM mensagem_cmd")

                results = self.cursor.fetchall()

                for parts in results:
                    self.dic_message_cmd.update(
                        {parts[0]: parts[1]})  # colocados dentro da lista as mensagens e os comandos
                return self.dic_message_cmd
            except Exception as e:
                logging.error(str(__name__) + ":erro get_cmds:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def get_quiz(self, cod: int):
        """

        :param cod:
        :return:
        """
        dicionario_quest = []
        logging.warning("get_quiz")
        if cod is None:
            cod = self.Numero_aleatorio_quiz()
        logging.warning(cod)

        if self.connection is not None:
            try:

                self.cursor.execute(
                    "SELECT pergunta, alternativa1, alternativa2, alternativa3, alternativa4, alternativa5, resposta "
                    "FROM quiz WHERE id = \'" + str(
                        cod) + "\'")

                results = self.cursor.fetchall()

                for parts in results:
                    quests = quest()
                    # result = str(cod)+"->"+str(res)

                    quests.set_pergunta(str(cod) + "->" + str(parts[0]))
                    quests.set_questA(str(parts[1]))
                    quests.set_questB(str(parts[2]))
                    quests.set_questC(str(parts[3]))
                    quests.set_questD(str(parts[4]))
                    quests.set_questE(str(parts[5]))
                    quests.set_resposta(str(parts[6]))
                    quests.set_cod(str(cod))
                    dicionario_quest.insert(0, quests.result().copy())

                logging.warning(dicionario_quest)
                return dicionario_quest[0].copy()
            except Exception as e:
                logging.error(str(__name__) + ":erro get_quiz:"+str(e))
                self.connection_on()
                return None
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
            return None

    def fechar_conexao(self):
        """

        :return:
        """
        logging.warning("fechar_conexao")
        if self.connection is not None:
            # Finaliza a conexão
            self.connection.close()
            logging.warning("conexao fechada")
        else:
            logging.error(str(__name__) + ":sem conexão com o banco de dados ")
