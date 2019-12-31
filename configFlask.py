import os.path
from config import DIR_SQLITE


DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DIR_SQLITE, 'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'chave_de_seguranca'
