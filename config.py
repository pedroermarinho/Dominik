import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

# DIR_DEFAULT = os.environ['HOME'] + "/.Dominik"
# DIR_DIC = dir_default + "/dictionary"
# DIR_DIC_YML = dir_default + "/dictionary/yml"

# try:
#     os.makedirs(DIR_DIC_YML)
# except OSError:
#     pass

DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DIR_DEFAULT, 'storage.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'chave_de_seguranca'
