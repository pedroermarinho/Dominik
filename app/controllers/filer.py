import sys
import os
import requests
import urllib3
import yaml
import json

dir_default = os.environ['HOME'] + "/.Dominik"
dir_dic_yml = dir_default + "/dictionary/yml"

try:
    os.makedirs(dir_dic_yml)
except OSError:
    pass


def download_yml(url, name):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    yml_data = yaml.load(response.data.decode('utf-8'))
    file = dir_dic_yml + "/" + yml_data["type"][0] + "/" + yml_data["language"][0]
    file_name = file + "/" + name + ".yml"
    print(file)
    try:
        os.makedirs(file)
    except OSError:
        pass
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
    file = dir_dic_yml + "/" + yml_data["type"][0] + "/" + yml_data["language"][0]
    file_name = file + "/" + name + ".yml"
    print(file)
    try:
        os.remove(file_name)
    except OSError:
        pass
    

def verify_file_yml(json_data):
    json_data = str(json_data)
    json_data = json_data.replace("\'", "\"")
    json_data = json.loads(json_data)
    file = dir_dic_yml + "/" + json_data["classification"] + "/" + json_data["language"]
    file_name = file + "/" + json_data["subcategory"] + ".yml"
    return os.path.isfile(file_name)
 



def verify_update_file_yml(json_data):
    json_data = str(json_data)
    json_data = json_data.replace("\'", "\"")
    json_data = json.loads(json_data)
    yml_url = json_data["url"]
    file = dir_dic_yml + "/" + json_data["classification"] + "/" + json_data["language"]
    file_name = file + "/" + json_data["subcategory"] + ".yml"

    if(os.path.isfile(file_name)):
        yaml_file = open(file_name, 'r', encoding='utf-8')
        yaml_Obj =  yaml.load(yaml_file)
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
