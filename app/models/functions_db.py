import pymysql
import random
from app.models.question import quest
from tokens.tokens import Tokens
import shutil
import os


class Database(object):
    print("banco_de_dados")
    keywords_wikipedia = []  # palavras chaves para pesquisas na wikipedia
    keywords_google = []  # palavras chaves para pesquisas no google
    definition_words = []  # palavras chaves para pesquisas no dicionario
    dic_cmd = {}  # criando um dicionario comandos
    dic_message_cmd = {}  # criando um dicionario comandos de menagem
    connection = None
    cursor = None

    def __init__(self):
        self.connection_on()

    def connection_on(self):

        try:
            # Abrimos uma conexão com o banco de dados:
            self.connection = pymysql.connect(host=Tokens.host, db=Tokens.db, user=Tokens.user,
                                              passwd=Tokens.passwd)
            # Cria um cursor:
            self.cursor = self.connection.cursor()
        except:
            print("erro conexão banco de dados")
            self.connection = None
            self.cursor = None

    def add_base_de_users(self, _id, nome=None):
        print("add_base_de_usuarios")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO base_de_usuarios VALUES (\'" + str(_id) + "\',\'" + str(
                    nome) + "\')")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.


            except:
                # print("Erro função-> add_base_de_usuarios")
                self.connection_on()
        else:
            print("sem conexão com o banco de dados ")

    def add_new_word(self, nome=None):
        print("add_nova_palavra")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO `novas_palavras`(`texto`) VALUES (\'" + str(
                    nome) + "\')")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.

            except:
                print("Erro função-> add_nova_palavra")
                self.connection_on()
        else:
            print("sem conexão com o banco de dados ")

    # adicione ponto positivo
    def add_positive_point(self, cod, last_question):
        print("add_positive_point")
        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO usuario  VALUES (\'" + str(cod) + "\',\'" + str(2) + "\'," + str(
                    last_question) + ")")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.
            except:
                try:
                    ultima_pergunta_banco = self.get_last_question(cod)

                    print(str(ultima_pergunta_banco) + "==" + str(last_question))

                    if ultima_pergunta_banco != last_question:
                        self.cursor.execute("UPDATE usuario SET pontuacao = (pontuacao + 2) WHERE id =\'" + str(
                            cod) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.
                        self.cursor.execute(
                            "UPDATE usuario SET ultima_pergunta = " + str(last_question) + " WHERE id =\'" + str(
                                cod) + "\'")
                        self.connection.commit()  # Efetua um commit no banco de dados.

                except:
                    print("Erro função-> add_pontucao_acetou")
                    self.connection_on()
        else:
            print("sem conexão com o banco de dados ")

    def add_negative_point(self, cod, ultima_pergunta):
        print("add_pontucao_errou id =" + str(cod) + " ultima_pergunta =" + str(ultima_pergunta))

        if self.connection is not None:
            try:
                self.cursor.execute("INSERT INTO usuario  VALUES (\'" + str(cod) + "\',\'" + str(-1) + "\'," + str(
                    ultima_pergunta) + ")")  # Executa o comando:
                self.connection.commit()  # Efetua um commit no banco de dados.
            except:

                try:
                    ultima_pergunta_banco = self.get_last_question(cod)

                    print(str(ultima_pergunta_banco) + "==" + str(ultima_pergunta))

                    if ultima_pergunta_banco != ultima_pergunta:
                        self.cursor.execute("UPDATE usuario SET pontuacao = (pontuacao - 1)   WHERE id =\'" + str(
                            cod) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.
                        self.cursor.execute(
                            "UPDATE usuario SET ultima_pergunta = (" + str(ultima_pergunta) + ") WHERE id =\'" + str(
                                cod) + "\'")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.

                except:
                    print("Erro função-> add_pontucao_errou")
                    self.connection_on()
        else:
            print("sem conexão com o banco de dados ")

    def get_last_question(self, cod):
        print("get_ultima_resposta")
        if self.connection is not None:
            try:
                self.connection.commit()  # Efetua um commit no banco de dados.
                self.cursor.execute("SELECT ultima_pergunta FROM usuario WHERE id = \'" + str(cod) + "\'")

                results = self.cursor.fetchall()
                print(results)
                result = None
                for res in results:
                    for resposta in res:
                        result = resposta

                print(result)
                return result
            except:
                print("Erro função-> get_ultima_resposta")
                self.connection_on()
                return 0
        else:
            print("sem conexão com o banco de dados ")

    def get_point(self, id):
        print("get_pontuacao")
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT pontuacao FROM usuario WHERE id = \'" + str(id) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(resposta)

                print(result)
                return result
            except:
                print("Erro função-> get_pontuacao")
                self.connection_on()
                return 0
        else:
            print("sem conexão com o banco de dados ")

    def add_curiosidade(self):
        print("add_curiosidade")
        if (self.connection is not None):
            # try:
            for _arquivo in os.listdir('assbot/ass_diversos/curiosidade'):  # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".txt"):
                    print(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    linhas = open('assbot/ass_diversos/curiosidade/' + _arquivo, 'r').readlines()  # vamos ler linhas
                    for linha in linhas:
                        linha = linha.replace('\n', '')
                        self.cursor.execute("INSERT INTO curiosidades (curiosidade) VALUES (\'" + str(
                            linha) + "\')")  # Executa o comando:
                        self.connection.commit()  # Efetua um commit no banco de dados.

                    shutil.move('assbot/ass_diversos/curiosidade/' + _arquivo,
                                'assbot/ass_diversos/curiosidade/ja_treinados/')  # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
            # except:
            #     print("Erro função-> treino curiosidade")
        else:
            print("sem conexão com o banco de dados ")

    def add_quiz(self):
        print("add_quiz")
        if (self.connection is not None):
            # try:
            for _arquivo in os.listdir('assbot/quiz'):  # percorrer todos os arquivos na pasta chats
                if _arquivo.endswith(".txt"):
                    print(_arquivo)  # mostrar o nome do aquivo que esta sendo lido
                    arquivo = open('assbot/quiz/' + _arquivo, 'r').readlines()
                    for comando in arquivo:  # percorendo todos os comandos
                        comando = comando.replace('\n', '')  # deletando as quebras de linha
                        parts = comando.split('||')  # separando mensaguem de comando // dicionario de comandos
                        self.cursor.execute(
                            "INSERT INTO quiz (pergunta, alternativa1, alternativa2, alternativa3, alternativa4, alternativa5, resposta) VALUES (\'" + str(
                                parts[0]) + "\',\'" + str(parts[1]) + "\',\'" + str(parts[2]) + "\',\'" + str(
                                parts[3]) + "\',\'" + str(parts[4]) + "\',\'" + str(parts[5]) + "\',\'" + str(
                                parts[6]) + "\')")
                        self.connection.commit()  # Efetua um commit no banco de dados.
                    shutil.move('assbot/quiz/' + _arquivo,
                                'assbot/quiz/ja_treinados/')  # mover os arquivos ja treinados para outra pasta para que não sejam treinados novamente
            # except:
            #     print("Erro função-> treino quiz")
        else:
            print("sem conexão com o banco de dados ")

    def Numero_aleatorio_piada(self):
        print("Numero_aleatorio_piada")
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM piadas")
                conts = self.cursor.fetchall()

                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except:
                print("erro numero aleatorio piada")
                self.connection_on()
                return int(0)
        else:
            print("sem conexão com o banco de dados ")
            return None

    def Numero_aleatorio_quiz(self):
        print("Numero_aleatorio_quiz")
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM quiz")
                conts = self.cursor.fetchall()
                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except:
                print("erro numero aleatorio quiz")
                self.connection_on()
                return int(1)
        else:
            print("sem conexão com o banco de dados ")
            return None

    def Numero_aleatorio_curiosidade(self):
        print("Numero_aleatorio_curiosidade")
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT COUNT(*) FROM curiosidades")
                conts = self.cursor.fetchall()
                cont = 0
                for con in conts:
                    for c in con:
                        cont = int(c)

                return int(random.randint(0, int(cont) - 1))
            except:
                print("erro numero aleatorio curiosidade")
                self.connection_on()
                return int(0)
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_piada(self, cod=None):
        print("get_piada")
        if cod is None:
            cod = self.Numero_aleatorio_piada()
        print(cod)
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT piada FROM piadas WHERE id = \'" + str(cod) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(cod) + ")" + str(resposta)

                return result
            except:
                print("erro get_piada")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_curiosidade(self, cod=None):
        print("get_curiosidade")
        if cod is None:
            cod = self.Numero_aleatorio_curiosidade()
        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT curiosidade FROM curiosidades WHERE id = \'" + str(cod) + "\'")

                results = self.cursor.fetchall()

                result = None
                for res in results:
                    for resposta in res:
                        result = str(cod) + ")" + str(resposta)
                return result
            except:
                print("erro get_quiz")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_definicao(self):
        print("get_definicao")

        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT texto FROM definicao")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.definition_words.insert(n, resposta)
                        n = n + 1
                return self.definition_words
            except:
                print("erro get_definicao")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_google(self):
        print("get_google")

        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT texto FROM google")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.keywords_google.insert(n, resposta)
                        n = n + 1
                return self.keywords_google
            except:
                print("erro get_google")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_wikipedia(self):
        print("get_wikipedia")

        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT texto FROM wikipedia")

                results = self.cursor.fetchall()

                n = 0
                for res in results:
                    for resposta in res:
                        self.keywords_wikipedia.insert(n, resposta)
                        n = n + 1
                return self.keywords_wikipedia
            except:
                print("erro get_wikipedia")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_cmds(self):
        print("get_cmds")

        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT texto , cmd FROM cmds")

                results = self.cursor.fetchall()

                for parts in results:
                    self.dic_cmd.update(
                        {parts[0]: parts[1]})  # colocados dentro da lista as mensagens e os comandos
                return self.dic_cmd
            except:
                print("erro get_cmds")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_mensagem_cmd(self):
        print("get_cmds")

        if (self.connection is not None):
            try:
                self.cursor.execute("SELECT cmd , texto  FROM mensagem_cmd")

                results = self.cursor.fetchall()

                for parts in results:
                    self.dic_message_cmd.update(
                        {parts[0]: parts[1]})  # colocados dentro da lista as mensagens e os comandos
                return self.dic_message_cmd
            except:
                print("erro get_cmds")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            return None

    def get_quiz(self, cod=None):
        dicionario_quest = []
        print("get_quiz")
        if cod is None:
            cod = self.Numero_aleatorio_quiz()
        print(cod)

        if (self.connection is not None):
            try:

                self.cursor.execute(
                    "SELECT pergunta, alternativa1, alternativa2, alternativa3, alternativa4, alternativa5, resposta FROM quiz WHERE id = \'" + str(
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

                print(dicionario_quest)
                return dicionario_quest[0].copy()
            except:
                print("erro get_quiz")
                self.connection_on()
                return None
        else:
            print("sem conexão com o banco de dados ")
            # return None

    def fechar_conexao(self):
        print("fechar_conexao")
        if (self.connection is not None):
            # Finaliza a conexão
            self.connection.close()
        else:
            print("sem conexão com o banco de dados ")