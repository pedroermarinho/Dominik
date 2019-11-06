import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time
from app.controllers.chat_bot import Dominik
from app.controllers.key_words import Palavra_Chave
from app.models.functions_db import Database
from app.controllers.commands import Comando
from app.controllers.arduino_cmd import arduino_cmd
from tokens.tokens import Tokens
from threading import Thread

arduino_comando = arduino_cmd()
cmds = Comando(arduino_comando)
main = Dominik(arduino_comando)
Palavra_Chave = Palavra_Chave()
base_de_dados = Database()

try:
    telegram = telepot.Bot(Tokens.chave_token_telegram)  # endereço de acesso do bot
except:
    print('erro de conexão')


# ---------------------------------------------------------------------------------------------------------------------------------

def recebendo_mensagem(msg):  # função que ira receber a mensagem

    content_type, chat_type, chat_id = telepot.glance(msg)

    texto = msg['text']  # captura somente o texto enviado

    # funçao para retorna o tipo da mensagem , tipo do chat e o Id do usuario que necessario para enviar mensagem
    Thread(target=base_de_dados.add_base_de_users,
           args=(str(chat_id), str(str(msg['from']['first_name']) + ' ' + msg['from']['last_name']),)).start()

    if cmds.comando(str(texto)) in {"CMD_LUZ_QUARTO_1", "CMD_LUZ_QUARTO_2", "CMD_LUZ_QUARTO_3", "CMD_LUZ_BANHEIRO_1",
                                    "CMD_LUZ_BANHEIRO_2", "CMD_LUZ_SALA", "CMD_LUZ_SALA_JANTAR", "CMD_LUZ_COZINHA",
                                    "CMD_LUZ_EXTERNA_ENTRADA", "CMD_LUZ_EXTERNA_SAIDA", "CMD_LUZ_EXTERNA_LATERAL",
                                    "CMD_TELEVISAO"}:

        Thread(target=Comandos, args=(chat_id, texto, cmds.comando(str(texto)),)).start()

    elif "cmd_quiz" == cmds.comando(str(texto)):
        Thread(target=Pergunta, args=(chat_id,)).start()

    else:
        Thread(target=chatbot, args=(msg,)).start()


# ---------------------------------------------------------------------------------------------------------------------------------
def chatbot(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    texto = msg['text']  # captura somente o texto enviado
    pergunta = main.mensagem_bot_pergunta(texto)  # função para transformar o texto e verificar sua entrada
    print(pergunta)  # mostra na tela a pergunta
    resposta = main.mensagem_bot_resposta(pergunta)  # função que captura a pergunta e gera uma resposta
    print(resposta)  # mostra a resposta na tela

    enviado = False
    while not enviado:
        try:
            telegram.sendMessage(int(chat_id), str(resposta).format(str(msg['from']['first_name']) + ' ' + str(
                msg['from']['last_name'])) + '\'')  # função para enviar mensagem para o usuario , o primeiro parametro
            # serve é id (endereço) do usuario e o segundo é a mensagem
            enviado = True
        except():
            print('Mensagem não enviada: tentando novamente')
            enviado = False


# ---------------------------------------------------------------------------------------------------------------------------------


def Comandos(chat_id=0, quest='Teste', comando="0"):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ligar', callback_data='cmd||1||' + str(comando) + '||0')],
        [InlineKeyboardButton(text='Desligar', callback_data='cmd||2||' + str(comando) + '||0')]
    ])

    telegram.sendMessage(int(chat_id), str(quest), reply_markup=keyboard)


# ---------------------------------------------------------------------------------------------------------------------------------

def Pergunta(chat_id=0):
    obj = base_de_dados.get_quiz()
    quest = obj[0]
    a = obj[1]
    b = obj[2]
    c = obj[3]
    d = obj[4]
    e = obj[5]
    resposta = obj[6]
    cod = obj[7]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='a ) ' + a,
                              callback_data='quiz||1||' + str(resposta) + '||' + str(cod))],
        [InlineKeyboardButton(text='B ) ' + b,
                              callback_data='quiz||2||' + str(resposta) + '||' + str(cod))],
        [InlineKeyboardButton(text='C ) ' + c,
                              callback_data='quiz||3||' + str(resposta) + '||' + str(cod))],
        [InlineKeyboardButton(text='D ) ' + d,
                              callback_data='quiz||4||' + str(resposta) + '||' + str(cod))],
        [InlineKeyboardButton(text='E ) ' + e,
                              callback_data='quiz||5||' + str(resposta) + '||' + str(cod))]
    ])

    telegram.sendMessage(int(chat_id), str(quest), reply_markup=keyboard)


# ---------------------------------------------------------------------------------------------------------------------------------

def Resposta(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    parts = query_data.split('||')
    tipo = parts[0]
    query_data = parts[1]
    respot = parts[2]
    cod = parts[3]

    if tipo == 'cmd':
        # ------------------------------------------------------------------------------

        if query_data == '1':
            telegram.answerCallbackQuery(query_id, text='Você apertou Ligar')

            if respot == "CMD_LUZ_QUARTO_1":
                Thread(target=arduino_comando.cmd_luz_quarto_1_on()).start()
            elif respot == "CMD_LUZ_QUARTO_2":
                Thread(target=arduino_comando.cmd_luz_quarto_2_on()).start()
            elif respot == "CMD_LUZ_QUARTO_3":
                Thread(target=arduino_comando.cmd_luz_quarto_3_on()).start()
            elif respot == "CMD_LUZ_BANHEIRO_1":
                Thread(target=arduino_comando.cmd_luz_banheiro_1_on()).start()
            elif respot == "CMD_LUZ_BANHEIRO_2":
                Thread(target=arduino_comando.cmd_luz_banheiro_2_on()).start()
            elif respot == "CMD_LUZ_SALA":
                Thread(target=arduino_comando.cmd_luz_sala_on()).start()
            elif respot == "CMD_LUZ_SALA_JANTAR":
                Thread(target=arduino_comando.cmd_luz_sala_jantar_on()).start()
            elif respot == "CMD_LUZ_COZINHA":
                Thread(target=arduino_comando.cmd_luz_cozinha_on()).start()
            elif respot == "CMD_LUZ_EXTERNA_ENTRADA":
                Thread(target=arduino_comando.cmd_luz_externa_entrada_on()).start()
            elif respot == "CMD_LUZ_EXTERNA_SAIDA":
                Thread(target=arduino_comando.cmd_luz_externa_saida_on()).start()
            elif respot == "CMD_LUZ_EXTERNA_LATERAL":
                Thread(target=arduino_comando.cmd_luz_externa_lateral_on()).start()
            elif respot == "CMD_TELEVISAO":
                Thread(target=arduino_comando.cmd_televisao_on()).start()
            else:
                telegram.sendMessage(chat_id, "Ops... Algo deu errado")

            telegram.sendMessage(chat_id, 'Olá {}, o(a) '.format(
                msg['from']['first_name'] + ' ' + msg['from']['last_name']) + respot + " foi ligada")
        # ------------------------------------------------------------------------------

        elif query_data == '2':
            telegram.answerCallbackQuery(query_id, text='Você apertou Desligar')

            if respot == "CMD_LUZ_QUARTO_1":
                Thread(target=arduino_comando.cmd_luz_quarto_1_off()).start()
            elif respot == "CMD_LUZ_QUARTO_2":
                Thread(target=arduino_comando.cmd_luz_quarto_2_off()).start()
            elif respot == "CMD_LUZ_QUARTO_3":
                Thread(target=arduino_comando.cmd_luz_quarto_3_off()).start()
            elif respot == "CMD_LUZ_BANHEIRO_1":
                Thread(target=arduino_comando.cmd_luz_banheiro_1_off()).start()
            elif respot == "CMD_LUZ_BANHEIRO_2":
                Thread(target=arduino_comando.cmd_luz_banheiro_2_off()).start()
            elif respot == "CMD_LUZ_SALA":
                Thread(target=arduino_comando.cmd_luz_sala_off()).start()
            elif respot == "CMD_LUZ_SALA_JANTAR":
                Thread(target=arduino_comando.cmd_luz_sala_jantar_off()).start()
            elif respot == "CMD_LUZ_COZINHA":
                Thread(target=arduino_comando.cmd_luz_cozinha_off()).start()
            elif respot == "CMD_LUZ_EXTERNA_ENTRADA":
                Thread(target=arduino_comando.cmd_luz_externa_entrada_off()).start()
            elif respot == "CMD_LUZ_EXTERNA_SAIDA":
                Thread(target=arduino_comando.cmd_luz_externa_saida_off()).start()
            elif respot == "CMD_LUZ_EXTERNA_LATERAL":
                Thread(target=arduino_comando.cmd_luz_externa_lateral_off()).start()
            elif respot == "CMD_TELEVISAO":
                Thread(target=arduino_comando.cmd_televisao_off()).start()
            else:
                telegram.sendMessage(chat_id, "Ops... Algo deu errado")

            telegram.sendMessage(chat_id, 'Olá {}, o(a) '.format(
                msg['from']['first_name'] + ' ' + msg['from']['last_name']) + respot + " foi Desligado")
        # ------------------------------------------------------------------------------

        else:

            telegram.sendMessage(chat_id, str(cod) + ') ' + "Algo deu errado")
        # ------------------------------------------------------------------------------

    elif tipo == 'quiz':

        if query_data == '1':
            telegram.answerCallbackQuery(query_id, text='Você apertou A')

            if respot == '1':

                telegram.sendMessage(chat_id, str(cod) + ') ' + 'Parabéns {}, você acertou 👏🏼👏🏼👏🏼 '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) + 2) + " pontos")

                Thread(target=base_de_dados.add_pontucao_acetou, args=(chat_id, int(str(cod) + str(1)),)).start()

            else:

                telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!!'.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

                Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(1)),)).start()

            # ------------------------------------------------------------------------------

        elif query_data == '2':
            telegram.answerCallbackQuery(query_id, text='Você apertou B')

            if respot == '2':

                telegram.sendMessage(chat_id, str(cod) + ') ' + 'Parabéns {}, você acertou 👏🏼👏🏼👏🏼 '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) + 2) + " pontos")

                Thread(target=base_de_dados.add_pontucao_acetou, args=(chat_id, int(str(cod) + str(2)),)).start()

            else:

                telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!!'.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

                Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(2)),)).start()

            # ------------------------------------------------------------------------------

        elif query_data == '3':
            telegram.answerCallbackQuery(query_id, text='Você apertou C')

            if respot == '3':

                telegram.sendMessage(chat_id, str(cod) + ') ' + 'Parabéns {}, você acertou 👏🏼👏🏼👏🏼 '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) + 2) + " pontos")

                Thread(target=base_de_dados.add_pontucao_acetou, args=(chat_id, int(str(cod) + str(3)),)).start()

            else:

                telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!!  '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

                Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(3)),)).start()

            # ------------------------------------------------------------------------------

        elif query_data == '4':
            telegram.answerCallbackQuery(query_id, text='Você apertou D')

            if respot == '4':

                telegram.sendMessage(chat_id, str(cod) + ') ' + 'Parabéns {}, você acertou 👏🏼👏🏼👏🏼 '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) + 2) + " pontos")

                Thread(target=base_de_dados.add_pontucao_acetou, args=(chat_id, int(str(cod) + str(4)),)).start()


            else:

                telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!! '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

                Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(4)),)).start()

            # ------------------------------------------------------------------------------

        elif query_data == '5':
            telegram.answerCallbackQuery(query_id, text='Você apertou E')

            if respot == '5':

                telegram.sendMessage(chat_id, str(cod) + ') ' + 'Parabéns {}, você acertou 👏🏼👏🏼👏🏼 '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) + 2) + " pontos")

                Thread(target=base_de_dados.add_pontucao_acetou, args=(chat_id, int(str(cod) + str(5)),)).start()

            else:

                telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!! '.format(
                    msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                    float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

                Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(5)),)).start()

            # ------------------------------------------------------------------------------

        else:

            telegram.sendMessage(chat_id, str(cod) + ') ' + '😓 Poxa, não foi dessa vez {}!!!'.format(
                msg['from']['first_name'] + ' ' + msg['from']['last_name']) + "\n Sua pontuação é de " + str(
                float(base_de_dados.get_point(chat_id)) - 1) + " pontos")

            Thread(target=base_de_dados.add_negative_point, args=(chat_id, int(str(cod) + str(0)),)).start()


# ------------------------------------------------------------------------------

# telegram.setWebhook()


# --------------------------------------------------------------------------------------------------------------------------------------------
def telegram_on():
    try:
        Thread(target=
               telegram.message_loop({'chat': recebendo_mensagem,
                                      'callback_query': Resposta},
                                     run_forever='Ligado...').run_as_thread()
               # funçao que fica esperando uma mensagem chega e tem como parametro a funcçao que será
               # executada quando ela chega
               ).start()
    except():
        print('Falha na conexão')


if __name__ == "__main__":
    telegram_on()
    while True:  # isso fara com que o programa fique rodando e na feche
        time.sleep(10)
