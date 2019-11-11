import sys
import os
import requests
import urllib3
import yaml

dir_default = os.environ['HOME'] + "/.Dominik"
dir_dic_yml = dir_default + "/dictionary/yml"
print(dir_default)

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
    pass


download_yml("https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/ai.yml","ia")

# link = "https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/ai.yml"
# file_name = directory_default+"/dictionary/yml/Formally/download.data"
# with open(file_name, "wb") as f:
#     print("Downloading %s" % file_name)
#     response = requests.get(link, stream=True)
#     total_length = response.headers.get('content-length')
#
#     if total_length is None:  # no content length header
#         f.write(response.content)
#     else:
#         dl = 0
#         total_length = int(total_length)
#         for data in response.iter_content(chunk_size=4096):
#             dl += len(data)
#             f.write(data)
#             done = int(50 * dl / total_length)
#             sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
#             sys.stdout.flush()
