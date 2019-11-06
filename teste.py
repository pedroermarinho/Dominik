
import yaml

import urllib3

http = urllib3.PoolManager()
response = http.request('GET', "https://pedroermarinho.github.io/Dominik-dic/src/yml/formally/PT-BR/conversations.yml")
data = response.data.decode('utf-8')
pythonObject = yaml.load(data)
print (pythonObject)