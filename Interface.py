import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from Principal import Main
import threading
import Telegram


class interface(QDialog):
    model = QStandardItemModel()
    main = Main()

    def __init__(self):
        super(interface, self).__init__()
        loadUi('tela_inicial.ui', self)
        self.setWindowTitle("Dominik")

        self.MensagemList.setModel(self.model)

        self.EnviarButton.clicked.connect(self.threadEnviar_on)


        self.TelegramButton.clicked.connect(self.threadTelegram_on)

    @pyqtSlot()
    def threadEnviar_on(self):
        print("threadEnviar_on")
        threading.Thread(target=self.Enviar_on).start()

    @pyqtSlot()
    def Enviar_on(self):
        print("enviar")
        mensagem = self.MensagemText.text()
        self.MensagemText.setText("")
        resposta = self.main.mensagem_bot_resposta(mensagem)
        item = QStandardItem("\nVocê: " + str(mensagem) + "\nDominik: " + str(resposta))
        self.model.appendRow(item)

    @pyqtSlot()
    def threadTelegram_on(self):
        try:
            print("threadEnviar_on")
            threading.Thread(target=self.Telegram_on).start()
        except:
            print("...")

    @pyqtSlot()
    def Telegram_on(self):
        Telegram.telegram_on()
        self.TelegramButton.disa


if __name__ == "__main__":
    print("ok")
    app = QApplication(sys.argv)
    widget = interface()
    widget.show()
    sys.exit(app.exec_())
