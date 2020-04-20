import sys
import os.path
import requests
import urllib3
import yaml

from config import DIR_DIC_YML

"""
    Gerenciamento de arquivos 
"""


def download_yml(url: str, name: str) -> bool:
    """
    Download de arquivos yml
    :param url: localização do arquivo yml
    :param name: Nome que será dado ao arquivo
    :return: True para finalizado e False para falha
    """

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    yml_data = yaml.load(response.data.decode('utf-8'))
    file = os.path.join(DIR_DIC_YML, yml_data["type"][0], yml_data["language"][0])
    file_name = os.path.join(file, name + ".yml")
    print(file)
    try:
        os.makedirs(file)
    except OSError as e:
        print(str(__name__) + ':def -> download_yml:' + str(e))
        pass
    try:
        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        return True
    except FileNotFoundError as e:
        print("arquivo não encontrado")
        print(str(__name__) + ':def -> download_yml:' + str(e))
        return False


def delete_yml(url: str, name: str) -> bool:
    """
    Delatar arquivos yml
    :param url: url do arquivo para recuperar dados utlizados para encontrar o diretorio correto
    :param name: Nome do arquivo a ser deletado
    :return: Não tem retorno
    """

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    yml_data = yaml.load(response.data.decode('utf-8'))
    file = os.path.join(DIR_DIC_YML, yml_data["type"][0], yml_data["language"][0])
    file_name = os.path.join(file, name + ".yml")
    print(file)
    try:
        os.remove(file_name)
        return True
    except OSError as e:
        print(str(__name__) + ':def -> delete_yml:' + str(e))
        return False


def verify_file_yml(data: dict) -> bool:
    """
    Verificar a existencia de uma arquivo yml
    :param data: Dados para encontrar o arquivo
    :return: retorna True se exitir e False caso não exista

    Exemplo:

    {
        'nome': 'IA',
        'url': 'https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/ai.yml',
        'type': 'yml',
        'language': 'PT-BR',
        'category': 'conversations',
        'subcategory': 'ai',
        'classification': 'formally'
    }
    """

    file = os.path.join(DIR_DIC_YML, data["classification"], data["language"])
    file_name = os.path.join(file, data["subcategory"] + ".yml")

    return os.path.isfile(file_name)


def verify_update_file_yml(data: dict) -> bool:
    """
    Verificar se um arquivo local está desatualizado em relação ao arquivo remoto
    :param data: Dados para encontrar o arquivo e realizar a comparação
    :return: retorna True se o arquivo estiver desatualizado e False caso esteja atulalizado

    Exemplo:

    {
        'nome': 'IA',
        'url': 'https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/ai.yml',
        'type': 'yml',
        'language': 'PT-BR',
        'category': 'conversations',
        'subcategory': 'ai',
        'classification': 'formally'
    }
    """

    yml_url = data["url"]
    file = os.path.join(DIR_DIC_YML, data["classification"], data["language"])
    file_name = os.path.join(file, data["subcategory"] + ".yml")

    try:
        with open(file_name, 'r', encoding='utf-8') as yaml_file:
            yaml_Obj = yaml.load(yaml_file)
    except FileNotFoundError as e:
        print(str(__name__) + ':def -> verify_update_file_yml:' + str(e))
        return False

    http = urllib3.PoolManager()
    response = http.request('GET', yml_url)
    yml_data = yaml.load(response.data.decode('utf-8'))

    if yaml_Obj != yml_data:
        return True
    else:
        return False


def list_file_yml_dic() -> list:
    """
    Lista de arquivos yml encontrados nos diretorios do dicionario
    :return: Retorna uma lista com todos os arquivos encontrados e as caractericas de cada um
    """
    result = []

    try:
        for _type in os.listdir(DIR_DIC_YML):
            for language in os.listdir(os.path.join(DIR_DIC_YML, _type)):
                for _file in os.listdir(os.path.join(DIR_DIC_YML, _type, language)):
                    if _file.endswith(".yml"):
                        file_name = os.path.join(DIR_DIC_YML, _type, language, _file)

                        try:
                            with open(file_name, 'r', encoding='utf-8') as yaml_file:
                                yaml_Obj = yaml.load(yaml_file)
                        except FileNotFoundError as e:
                            print(str(__name__) + ':def -> list_file_yml_dic:' + str(e))
                            return result

                        result.append({
                            'categories': yaml_Obj['categories'][0],
                            'type': yaml_Obj['type'][0],
                            'language': yaml_Obj['language'][0],
                            'file_url': file_name
                        })
        return result
    except IOError as e:
        print(str(__name__) + ':def -> list_file_yml_dic:' + str(e))
        return result


if __name__ == '__main__':

    for index, i in enumerate(list_file_yml_dic()):
        print(index, i)
    pass
