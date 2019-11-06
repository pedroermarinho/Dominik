from datetime import datetime
from app.controllers.key_words import Palavra_Chave
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from app.models.functions_db import Database
from app.controllers.arduino_cmd import arduino_cmd
from threading import Thread

class Comando:
    print('class comando')

    palavra_chave = Palavra_Chave()
    base_de_dados = Database()
    global arduino_comando

    def __init__(self, _arduino=arduino_cmd()):
        self.arduino_comando = _arduino

    dicionario_cmd = {}  # criando um dicionario
    comandos = None

    dicionario_cmd = base_de_dados.get_cmds()

    def comando(self, cmd):  # pasar o comando // função

        try:  # except para probrelmas
            result = process.extract(cmd, self.dicionario_cmd.keys(), scorer=fuzz.token_sort_ratio, limit=1)

            for y, i in result:
                comando = y
                confianca = i

            print("comando->" + comando)
            print("nivel de confiança->" + str(confianca))

            if (int(confianca) > 80):
                return self.dicionario_cmd[comando]  # resultado do comando
            else:
                return None
        except:  # caso não tenha
            print("erro piada")
            return None  # retorna a nada

    def Lista_comandos(self):  # função para lista os comandos
        result = ''
        for cmd, msg in self.base_de_dados.get_mensagem_cmd():
            if (cmd == 'msg_cmd'):
                result = msg
        return result

    def executar_cmd(self, cmd):  # função para execuatr os comandos
        if cmd == '/start':
            resultado = None
            for cmd, msg in self.base_de_dados.get_mensagem_cmd():
                if (cmd == 'msg_start'):
                    resultado = msg
            return resultado
        if cmd == 'cmd_hora':
            data = datetime.now()
            return 'São ' + str(data.hour) + ' horas e ' + str(data.minute) + ' minutos'
        elif cmd == 'cmd_data':
            data = datetime.now()
            return 'Hoje é ' + str(data.day) + ' de ' + str(data.month)
        elif cmd == 'cmd_lista_comandos':
            return self.Lista_comandos()
        elif cmd == 'cmd_treinar':
            # main.treinar()
            return 'treinado'
        elif cmd == 'cmd_piadas':
            return self.base_de_dados.get_piada()
        elif cmd == 'cmd_Charadas':
            return self.palavra_chave.Charada()
        elif cmd == 'cmd_citacoes':
            return self.palavra_chave.citacao()
        elif cmd == 'cmd_curiosidades':
            return self.base_de_dados.get_curiosidade()

        # ------------------------------------------------------------------------------
        #     Thread(target=arduino_comando.cmd_televisao_off()).start()

        elif cmd == 'cmd_luz_quarto_1_on':
            Thread(target=self.arduino_comando.cmd_luz_quarto_1_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_quarto_1_off':
            Thread(target=self.arduino_comando.cmd_luz_quarto_1_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_quarto_2_on':
            Thread(target=self.arduino_comando.cmd_luz_quarto_2_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_quarto_2_off':
            Thread(target=self.arduino_comando.cmd_luz_quarto_2_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_quarto_3_on':
            Thread(target=self.arduino_comando.cmd_luz_quarto_3_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_quarto_3_off':
            Thread(target=self.arduino_comando.cmd_luz_quarto_3_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_banheiro_1_on':
            Thread(target=self.arduino_comando.cmd_luz_banheiro_1_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_banheiro_1_off':
            Thread(target=self.arduino_comando.cmd_luz_banheiro_1_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_banheiro_2_on':
            Thread(target=self.arduino_comando.cmd_luz_banheiro_2_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_banheiro_2_off':
            Thread(target=self.arduino_comando.cmd_luz_banheiro_2_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_sala_on':
            Thread(target=self.arduino_comando.cmd_luz_sala_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_sala_off':
            Thread(target=self.arduino_comando.cmd_luz_sala_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_sala_jantar_on':
            Thread(target=self.arduino_comando.cmd_luz_sala_jantar_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_sala_jantar_off':
            Thread(target=self.arduino_comando.cmd_luz_sala_jantar_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_cozinha_on':
            Thread(target=self.arduino_comando.cmd_luz_cozinha_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_cozinha_off':
            Thread(target=self.arduino_comando.cmd_luz_cozinha_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_externa_entrada_on':
            Thread(target=self.arduino_comando.cmd_luz_externa_entrada_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_externa_entrada_off':
            Thread(target=self.arduino_comando.cmd_luz_externa_entrada_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_externa_saida_on':
            Thread(target=self.arduino_comando.cmd_luz_externa_saida_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_externa_saida_off':
            Thread(target=self.arduino_comando.cmd_luz_externa_saida_off()).start()
            return 'OK'

        elif cmd == 'cmd_luz_externa_lateral_on':
            Thread(target=self.arduino_comando.cmd_luz_externa_lateral_on()).start()
            return 'OK'
        elif cmd == 'cmd_luz_externa_lateral_off':
            Thread(target=self.arduino_comando.cmd_luz_externa_lateral_off()).start()
            return 'OK'

        elif cmd == 'cmd_televisao_on':
            Thread(target=self.arduino_comando.cmd_televisao_on()).start()
            return 'OK'
        elif cmd == 'cmd_televisao_off':
            Thread(target=self.arduino_comando.cmd_televisao_off()).start()
            return 'OK'
        else:
            return None
