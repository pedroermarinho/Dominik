class quest(object):

    def __init__(self):
        self.pergunta = None
        self.questA = None
        self.questB = None
        self.questC = None
        self.questD = None
        self.questE = None
        self.resposta = None
        self.cod = None

    # --------------------------------------------------------------------------------------------------------------------------------
    def get_pergunta(self):
        return self.pergunta

    def get_questA(self):
        return self.questA

    def get_questB(self):
        return self.questB

    def get_questC(self):
        return self.questC

    def get_questD(self):
        return self.questD

    def get_questE(self):
        return self.questE

    def get_resposta(self):
        return self.resposta

    def get_cod(self):
        return self.cod

    # -------------------------------------------------------------------------------------------------------------------------------

    def set_pergunta(self, text=None):
        self.pergunta = text

    def set_questA(self, text=None):
        self.questA = text

    def set_questB(self, text=None):
        self.questB = text

    def set_questC(self, text=None):
        self.questC = text

    def set_questD(self, text=None):
        self.questD = text

    def set_questE(self, text=None):
        self.questE = text

    def set_resposta(self, text=None):
        self.resposta = text

    def set_cod(self, text=None):
        self.cod = text

    # --------------------------------------------------------------------------------------------------------------------------------
    def inserir(self, pergunta=None, questA=None, questB=None, questC=None, questD=None, questE=None, resposta=None,
                cod=None):
        self.pergunta = pergunta
        self.questA = questA
        self.questB = questB
        self.questC = questC
        self.questD = questD
        self.questE = questE
        self.resposta = resposta
        self.cod = cod

    def result(self):
        dic = []
        dic.insert(0, self.pergunta)
        dic.insert(1, self.questA)
        dic.insert(2, self.questB)
        dic.insert(3, self.questC)
        dic.insert(4, self.questD)
        dic.insert(5, self.questE)
        dic.insert(6, self.resposta)
        dic.insert(7, self.cod)
        return dic
