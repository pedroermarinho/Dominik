# -*- coding:utf-8  -*-
import logging
import wikipedia
from urllib.request import urlopen
from bs4 import BeautifulSoup
import googlesearch

from app.controllers import functions_db


class KeyWords(object):
    wikipedia.set_lang('pt')  # determina que todas as pesquisas da wikipedia sejam em portugues

    def __init__(self):
        print(str(__name__) + '__init__')
        self.base_de_dados = functions_db.Database()
        self.palavras_chaves_wikipedia = self.base_de_dados.get_wikipedia()  # pegar as palavras chaves de pesquisa
        # da wikipedia no banco de dados
        self.palavras_chaves_google = self.base_de_dados.get_google()  # pegar as palavras chaves de pesquisa do
        # google no banco de dados
        self.palavras_chaves_definicao = self.base_de_dados.get_definicao()  # pegar as palavras chaves de pesquisa
        # de definicao no banco de dados

    def pesquisa_na_wikipedia(self, text: str) -> str:
        """
        Função para verificar se a um pedido de pesquisa para a wikipedia

        :param text: Texto a ser verificado
        :return: String
        """
        print("wiki")

        result = None  # resultado
        if self.palavras_chaves_wikipedia is not None:
            for chave in self.palavras_chaves_wikipedia:  # percorrer as palavras chaves
                print(chave)
                if text.lower().startswith(chave.lower()):  # verifrica se texto começa com alguma palavra chave
                    result = text.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada

        if result is not None:  # verifica se result não é nulo
            result = self.wikipedia_cmd(str(result))

        # if result is None:
        #     # return 'Não foi poss�vel fazer a pesquisa'
        #     return None
        # else:
        return result

    @staticmethod
    def wikipedia_cmd(text: str):
        """
        Função para pesquisar na wikipedia
        :param text: Texto a ser pesquisado
        :return: String ou None
        """
        try:
            logging.warning(str(__name__) + ':pesquisando')
            result = wikipedia.summary(wikipedia.search(text)[0], sentences=2)  # retornara ao primeiro resultado
        except:
            logging.error(str(__name__) + ':\nerro função: def wikipedia_cmd\n')
            result = None
        return result

    def pesquisa_no_google(self, text: str) :  #
        """
        Função para pesquisar no google
        :param text: Texto a ser pesquisado
        :return: String
        """

        result = None  # resultado
        if self.palavras_chaves_google is not None:
            for chave in self.palavras_chaves_google:  # percorrer as palavras chaves
                if text.lower().startswith(chave.lower()):  # verifica se texto começa com alguma palavra chave
                    result = text.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada
        if result is not None:  # vrefica se result não é nulo
            try:
                url = ""
                logging.warning(str(__name__) + ':pesquisando')
                for url in googlesearch.search(text, stop=1):
                    result = url
                    break
                html = urlopen(url)
                res = BeautifulSoup(html.read(), "html5lib")
                tags = res.findAll("p")
                result = result + "\n" + tags.__getitem__(0).getText()
                return result  # retornara ao primeiro resultado
            except:
                logging.error(str(__name__) + ':\nerro função: def pesquisa_na_wikipedia\n')
                return 'Não foi possivel fazer a pesquisa'
        return None

    def pesquisa_definicao(self, text: str) -> str:
        """
        Função para verificar se a um pedido de pesquisa de definições
        :param text: Texto a ser verificado
        :return: String
        """
        print("definição")

        result = None  # resultado
        print(self.palavras_chaves_definicao)
        if self.palavras_chaves_definicao is not None:
            for chave in self.palavras_chaves_definicao:  # percorrer as palavras chaves
                if text.lower().startswith(chave.lower()):  # verifica se texto começa com alguma palavra chave
                    result = text.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada
                    result = result.replace(" ", '')

        if result is not None:  # verifica se result não é nulo
            result = self.definicao(result)

        # if result is None:
        #     return 'Não foi poss�vel fazer a pesquisa'
        # else:
        return result

    @staticmethod
    def definicao(text: str):
        """
        Função para pesquisar no significados.com.br
        :param text: Texto a ser pesquisado
        :return:
        """
        try:
            logging.warning(str(__name__) + ':pesquisando definição->' + text)
            html = urlopen("https://www.significados.com.br/?s=" + text)
            res = BeautifulSoup(html.read(), "html5lib")
            tags = res.findAll("p")
            result = tags.__getitem__(1).getText()
            return result
        except:
            logging.error(str(__name__) + ':\nerro função: definicao\n')
            result = None
        return result
