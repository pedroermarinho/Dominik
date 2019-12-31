# -*- coding:utf-8  -*-
import logging
from Arduino import Arduino
import time
import os
import threading
import platform


class ArduinoCMD:
    """
    Classe para controle de hardware do arduino uno
    """
    logging.warning(__name__)

    def __init__(self):
        """
            inicialização dos pinos
        """
        print(str(__name__)+'__init__')
        self.board = None
        self.LUZ_BANHEIRO_1 = int(9)  # ok
        self.LUZ_BANHEIRO_2 = int(12)  # ok
        self.LUZ_COZINHA = int(5)  # ok
        self.LUZ_QUARTO_1 = int(13)  # ok
        self.LUZ_QUARTO_2 = int(6)  # ok
        self.LUZ_QUARTO_3 = int(7)  # ok
        self.LUZ_SALA = int(11)  # ok
        self.LUZ_SALA_JANTAR = int(2)  # off
        self.LUZ_EXTERNA_ENTRADA = int(2)  # off
        self.LUZ_EXTERNA_SAIDA = int(2)  # off
        self.LUZ_EXTERNA_LATERAL = int(2)  # off
        self.TELEVISAO = int(2)  # off
        self.conexao()

    def conexao(self):
        try:
            self.board.digitalRead(0)
        except:
            if platform.system() in "Windows":
                logging.warning(str(__name__) + ':'+str(platform.system()))
                try:
                    self.board = Arduino("115200", port='COM1')  # plugged in via USB, serial com at rate 115200
                except:
                    try:
                        self.board = Arduino("115200", port='COM2')  # plugged in via USB, serial com at rate 115200
                    except:
                        try:
                            self.board = Arduino("115200", port="COM3")  # plugged in via USB, serial com at rate 115200
                        except:
                            try:
                                self.board = Arduino("115200",
                                                     port="COM4")  # plugged in via USB, serial com at rate 115200
                            except:
                                try:
                                    self.board = Arduino("115200",
                                                         port="COM5")  # plugged in via USB, serial com at rate 115200
                                except:
                                    try:
                                        self.board = Arduino(
                                            baud="115200")  # plugged in via USB, serial com at rate 115200
                                    except:
                                        pass
            else:
                try:
                    os.system("ls -lh /dev/ttyACM0")
                    self.board = Arduino(port='/dev/ttyACM0')  # plugged in via USB, serial com at rate 115200
                except:
                    try:
                        os.system("ls -lh /dev/ttyACM1")
                        self.board = Arduino(port='/dev/ttyACM1')  # plugged in via USB, serial com at rate 115200
                    except:
                        try:
                            os.system("ls -lh /dev/ttyUSB1")
                            self.board = Arduino(port="/dev/ttyUSB1")  # plugged in via USB, serial com at rate 115200
                        except:
                            try:
                                os.system("ls -lh /dev/ttyUSB0")
                                self.board = Arduino(
                                    port="/dev/ttyUSB0")  # plugged in via USB, serial com at rate 115200
                            except:
                                try:
                                    self.board = Arduino(baud="115200")  # plugged in via USB, serial com at rate 115200
                                except:
                                    pass
            try:

                self.board.pinMode(self.LUZ_BANHEIRO_1, "OUTPUT")
                self.board.pinMode(self.LUZ_BANHEIRO_2, "OUTPUT")
                self.board.pinMode(self.LUZ_COZINHA, "OUTPUT")
                self.board.pinMode(self.LUZ_QUARTO_1, "OUTPUT")
                self.board.pinMode(self.LUZ_QUARTO_2, "OUTPUT")
                self.board.pinMode(self.LUZ_QUARTO_3, "OUTPUT")
                self.board.pinMode(self.LUZ_SALA, "OUTPUT")
                self.board.pinMode(self.LUZ_SALA_JANTAR, "OUTPUT")
                self.board.pinMode(self.LUZ_EXTERNA_ENTRADA, "OUTPUT")
                self.board.pinMode(self.LUZ_EXTERNA_SAIDA, "OUTPUT")
                self.board.pinMode(self.LUZ_EXTERNA_LATERAL, "OUTPUT")
                self.board.pinMode(self.TELEVISAO, "OUTPUT")

            except:
                logging.error(str(__name__)+":erro conexão arduino:")


    def cmd_luz_quarto_1_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_1, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_1_on:"+str(e))
            self.conexao()

    def cmd_luz_quarto_1_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_1, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_1_off:"+str(e))
            self.conexao()

    def cmd_luz_quarto_2_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_2, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_2_on:"+str(e))
            self.conexao()

    def cmd_luz_quarto_2_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_2, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_2_off:"+str(e))
            self.conexao()

    def cmd_luz_quarto_3_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_3, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_3_on:"+str(e))
            self.conexao()

    def cmd_luz_quarto_3_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_QUARTO_3, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_quarto_3_off:"+str(e))
            self.conexao()

    def cmd_luz_banheiro_1_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_BANHEIRO_1, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_banheiro_1_on:"+str(e))
            self.conexao()

    def cmd_luz_banheiro_1_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_BANHEIRO_1, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_banheiro_1_off:"+str(e))
            self.conexao()

    def cmd_luz_banheiro_2_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_BANHEIRO_2, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_banheiro_2_on:"+str(e))
            self.conexao()

    def cmd_luz_banheiro_2_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_BANHEIRO_2, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_banheiro_2_off:"+str(e))
            self.conexao()

    def cmd_luz_sala_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_SALA, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_sala_on:"+str(e))
            self.conexao()

    def cmd_luz_sala_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_SALA, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_sala_off:"+str(e))
            self.conexao()

    def cmd_luz_cozinha_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_COZINHA, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_cozinha_on:"+str(e))
            self.conexao()

    def cmd_luz_cozinha_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_COZINHA, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_cozinha_off")
            self.conexao()

    def cmd_luz_sala_jantar_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_SALA_JANTAR, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_sala_jantar_on:"+str(e))
            self.conexao()

    def cmd_luz_sala_jantar_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_SALA_JANTAR, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_sala_jantar_off:"+str(e))
            self.conexao()

    def cmd_luz_externa_entrada_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_ENTRADA, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_entrada_on:"+str(e))
            self.conexao()

    def cmd_luz_externa_entrada_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_ENTRADA, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_entrada_off:"+str(e))
            self.conexao()

    def cmd_luz_externa_saida_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_SAIDA, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_saida_on:"+str(e))
            self.conexao()

    def cmd_luz_externa_saida_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_SAIDA, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_saida_off:"+str(e))
            self.conexao()

    def cmd_luz_externa_lateral_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_LATERAL, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_lateral_on:"+str(e))
            self.conexao()

    def cmd_luz_externa_lateral_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.LUZ_EXTERNA_LATERAL, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_luz_externa_lateral_off:"+str(e))
            self.conexao()

    def cmd_televisao_on(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.TELEVISAO, "HIGH")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_televisao_on:"+str(e))
            self.conexao()

    def cmd_televisao_off(self):
        self.conexao()
        try:
            self.board.digitalWrite(self.TELEVISAO, "LOW")
        except IOError as e:
            logging.error(str(__name__)+":erro arduino ->cmd_televisao_off:"+str(e))
            self.conexao()

    def status(self):
        status = {}
        try:

            status.update({"LUZ_BANHEIRO_1": bool(self.board.digitalRead(self.LUZ_BANHEIRO_1))})

            status.update({"LUZ_BANHEIRO_2": bool(self.board.digitalRead(self.LUZ_BANHEIRO_2))})

            status.update({"LUZ_COZINHA": bool(self.board.digitalRead(self.LUZ_COZINHA))})

            status.update({"LUZ_QUARTO_1": bool(self.board.digitalRead(self.LUZ_QUARTO_1))})

            status.update({"LUZ_QUARTO_2": bool(self.board.digitalRead(self.LUZ_QUARTO_2))})

            status.update({"LUZ_QUARTO_3": bool(self.board.digitalRead(self.LUZ_QUARTO_3))})

            status.update({"LUZ_SALA": bool(self.board.digitalRead(self.LUZ_SALA))})

            status.update({"LUZ_SALA_JANTAR LUZ": bool(self.board.digitalRead(self.LUZ_SALA_JANTAR))})

            status.update({"LUZ_EXTERNA_ENTRADA LUZ": bool(self.board.digitalRead(self.LUZ_EXTERNA_ENTRADA))})

            status.update({"LUZ_EXTERNA_SAIDA LUZ": bool(self.board.digitalRead(self.LUZ_EXTERNA_SAIDA))})

            status.update({"LUZ_EXTERNA_LATERAL LUZ": bool(self.board.digitalRead(self.LUZ_EXTERNA_LATERAL))})

            status.update({"TELEVISAO": bool(self.board.digitalRead(self.TELEVISAO))})

        except IOError as e:
            self.conexao()
            logging.error(str(__name__)+":Erro:status:"+str(e))

        logging.warning(str(__name__) + ':'+str(status))
        return status


if __name__ == "__main__":
    arduino2 = ArduinoCMD()
    while True:
        arduino2.cmd_luz_banheiro_1_on()  # certo
        arduino2.cmd_luz_banheiro_2_on()  # certo
        arduino2.cmd_luz_cozinha_on()  # certo
        arduino2.cmd_luz_quarto_1_on()  # certo
        arduino2.cmd_luz_quarto_2_on()  # certo
        arduino2.cmd_luz_quarto_3_on()  # certo
        arduino2.cmd_luz_sala_on()  # certo

        time.sleep(2)
        arduino2.status()
        arduino2.cmd_luz_banheiro_1_off()
        arduino2.cmd_luz_banheiro_2_off()
        arduino2.cmd_luz_cozinha_off()
        arduino2.cmd_luz_quarto_1_off()
        arduino2.cmd_luz_quarto_2_off()
        arduino2.cmd_luz_quarto_3_off()
        arduino2.cmd_luz_sala_off()

        time.sleep(2)
        arduino2.status()
