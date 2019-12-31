# -*- coding:utf-8  -*-
import logging
from datetime import datetime
from controller import key_words
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from controller import functions_db
from threading import Thread


class Comando:
    logging.warning(__name__)

    def __init__(self, _arduino):
        print(str(__name__) + '__init__')
        self.arduino_comando = _arduino
        self.palavra_chave = key_words.PalavraChave()
        self.base_de_dados = functions_db.Database()
        self.comandos = None
        self.dicionario_cmd = self.base_de_dados.get_cmds()

    # dicionario_cmd = {}  # criando um dicionario

    def comando(self, cmd):  # pasar o comando // função

        global comando, confianca
        try:  # except para probrelmas
            result = process.extract(cmd, self.dicionario_cmd.keys(), scorer=fuzz.token_sort_ratio, limit=1)

            for y, i in result:
                comando = y
                confianca = i

            logging.warning(str(__name__) + ':comando->' + str(comando))
            logging.warning(str(__name__) + ':nivel de confiança->' + str(confianca))

            if (int(confianca) > 80):
                return self.dicionario_cmd[comando]  # resultado do comando
            else:
                return None
        except:  # caso não tenha
            print("erro piada")
            return None  # retorna a nada

    def Lista_comandos(self):  # função para lista os comandos
        result = None
        for cmd, msg in self.base_de_dados.get_mensagem_cmd():
            if cmd == 'msg_cmd':
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
