import sys
import os.path
import requests
import urllib3
import yaml
import json

from config import DIR_DIC_YML


def download_yml(url, name):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    yml_data = yaml.load(response.data.decode('utf-8'))
    file = os.path.join(DIR_DIC_YML, yml_data["type"][0], yml_data["language"][0])
    file_name = os.path.join(file, name + ".yml")
    print(file)
    # try:
    #     os.makedirs(file)
    # except OSError as e:
    #     pass
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


def delete_yml(url, name):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    yml_data = yaml.load(response.data.decode('utf-8'))
    file = os.path.join(DIR_DIC_YML, yml_data["type"][0], yml_data["language"][0])
    file_name = os.path.join(file, name + ".yml")
    print(file)
    try:
        os.remove(file_name)
    except OSError as e:
        pass


def verify_file_yml(json_data):
    json_data = str(json_data)
    json_data = json_data.replace("\'", "\"")
    json_data = json.loads(json_data)
    file = os.path.join(DIR_DIC_YML, json_data["classification"], json_data["language"])
    file_name = os.path.join(file, json_data["subcategory"] + ".yml")
    return os.path.isfile(file_name)


def verify_update_file_yml(json_data):
    json_data = str(json_data)
    json_data = json_data.replace("\'", "\"")
    json_data = json.loads(json_data)
    yml_url = json_data["url"]
    file = os.path.join(DIR_DIC_YML, json_data["classification"], json_data["language"])
    file_name = os.path.join(file, json_data["subcategory"] + ".yml")

    if (os.path.isfile(file_name)):
        yaml_file = open(file_name, 'r', encoding='utf-8')
        yaml_Obj = yaml.load(yaml_file)
        yaml_file.close()

        http = urllib3.PoolManager()
        response = http.request('GET', yml_url)
        yml_data = yaml.load(response.data.decode('utf-8'))
        if (yaml_Obj != yml_data):
            return True
        else:
            return False
    else:
        return False


def list_file_yml_dic():
    result = []
    file_name = ''

    try:
        for _type in os.listdir(DIR_DIC_YML):
            # print(_type)
            for language in os.listdir(os.path.join(DIR_DIC_YML, _type)):
                # print(language)
                for _file in os.listdir(os.path.join(DIR_DIC_YML, _type, language)):
                    if _file.endswith(".yml"):
                        # print(_file)
                        file_name = os.path.join(DIR_DIC_YML, _type, language, _file)
                        yaml_file = open(file_name, 'r', encoding='utf-8')
                        yaml_Obj = yaml.load(yaml_file)
                        yaml_file.close()
                        # print(yaml_Obj)
                        result.append({
                            'categories': yaml_Obj['categories'][0],
                            'type': yaml_Obj['type'][0],
                            'language': yaml_Obj['language'][0],
                            'file_url': file_name
                        })
        return result
    except IOError as e:
        print("Erro função-> treino" + str(e))
    pass


if __name__ == '__main__':

    for index, i in enumerate(list_file_yml_dic()):
        print(index, i)
    pass
