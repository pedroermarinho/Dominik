import wikipedia
from urllib.request import urlopen
from bs4 import BeautifulSoup
from app.models.functions_db import Database


class Palavra_Chave:
    base_de_dados = Database()

    wikipedia.set_lang('pt')  # determina que todas as pesquisas da wikipedia sejam em portugues
    palavras_chaves_wikipedia = []  # palavras chaves para pesquisas na wikipedia
    palavras_chaves_google = []  # palavras chaves para pesquisas na wikipedia
    palavras_chaves_definicao = []  # palavras chaves para pesquisas na wikipedia

    palavras_chaves_wikipedia = base_de_dados.get_wikipedia()  # pegar as palavras chaves de pesquisa da wikipedia no banco de dados

    palavras_chaves_google = base_de_dados.get_google()  # pegar as palavras chaves de pesquisa do google no banco de dados

    palavras_chaves_definicao == base_de_dados.get_definicao()  # pegar as palavras chaves de pesquisa de definicao no banco de dados

    def pesquisa_na_wikipedia(self, texto):  # função para pesquisa na wikipedia
        print("wiki")

        result = None  # resultado

        for chave in self.palavras_chaves_wikipedia:  # percorrer as palavras chaves
            if texto.lower().startswith(chave.lower()):  # verifica se texto começa com alguma palavra chave
                result = texto.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada
        if result is not None:  # verifica se result não é nulo
            try:
                print('pesquisando')
                return wikipedia.summary(wikipedia.search(result)[0], sentences=2)  # retornara ao primeiro resultado
            except:
                print('\nerro função: def pesquisa_na_wikipedia\n')
                return 'Não foi poss�vel fazer a pesquisa'

    def pesquisa_no_google(self, texto):  # função para pesquisa no google

        #
        #
        # result = None  # resultado
        #
        # for chave in self.palavras_chaves_google:  # percorrer as palavras chaves
        #     if texto.lower().startswith(chave.lower()):  # verifica se texto começa com alguma palavra chave
        #         result = texto.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada
        # if result is not None:  # vrefica se result não é nulo
        #     try:
        #         print('pesquisando')
        #         for url in search(texto,stop=1):
        #             result=url
        #             break
        #         html = urlopen(url)
        #         res = BeautifulSoup(html.read(), "html5lib")
        #         tags = res.findAll("p")
        #         result = result+"\n"+tags.__getitem__(0).getText()
        #         return result  # retornara ao primeiro resultado
        #     except:
        #         print('\nerro função: def pesquisa_na_wikipedia\n')
        #         return 'Não foi possivel fazer a pesquisa'
        return None

    def pesquisa_definicao(self, texto):  # função para pesquisa na wikipedia
        print("definição")

        result = None  # resultado
        print(self.palavras_chaves_definicao)
        for chave in self.palavras_chaves_definicao:  # percorrer as palavras chaves
            if texto.lower().startswith(chave.lower()):  # verifica se texto começa com alguma palavra chave
                result = texto.lower().replace(chave.lower(), '')  # texto atual menos a chave utilizada
                result = result.replace(" ", '')
        if result is not None:  # vrefica se result não é nulo
            try:
                print('pesquisando definição->' + result)
                html = urlopen("https://www.significados.com.br/?s=" + str(result))
                res = BeautifulSoup(html.read(), "html5lib")
                tags = res.findAll("p")
                result = tags.__getitem__(1).getText()
                return result
            except:
                print('\npesquisa_definicaon')
                return 'Não foi possivel fazer a pesquisa'

    def wikipedia(self, text):
        try:
            print('pesquisando')
            result = wikipedia.summary(wikipedia.search(text)[0], sentences=2)  # retornara ao primeiro resultado
        except:
            print('\nerro função: def wikipedia\n')
            result = None
        return result

    def definicao(self, text):
        try:
            print('pesquisando definição->' + text)
            html = urlopen("https://www.significados.com.br/?s=" + text)
            res = BeautifulSoup(html.read(), "html5lib")
            tags = res.findAll("p")
            result = tags.__getitem__(1).getText()
            return result
        except:
            print('\nerro função: definicao\n')
            result = None
        return result
