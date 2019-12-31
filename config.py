import os.path

DIR_DEFAULT = os.path.join(os.environ['HOME'], '.Dominik')
DIR_DIC = os.path.join(DIR_DEFAULT, 'dictionary')
DIR_DIC_YML = os.path.join(DIR_DEFAULT, 'dictionary', 'yml')
DIR_SQLITE = os.path.join(DIR_DEFAULT, 'sqlite')
DIR_LOG = os.path.join(DIR_DEFAULT, 'log')
DATABASE_URI_CHAT_DEFAULT = 'sqlite:///' + os.path.join(DIR_SQLITE, 'chat.db')

try:
    os.makedirs(DIR_DEFAULT, exist_ok=True)
    os.makedirs(DIR_DIC, exist_ok=True)
    os.makedirs(DIR_DIC_YML, exist_ok=True)
    os.makedirs(os.path.join(DIR_DIC_YML, 'formally'), exist_ok=True)
    os.makedirs(os.path.join(DIR_DIC_YML, 'informally'), exist_ok=True)
    os.makedirs(DIR_SQLITE, exist_ok=True)
    os.makedirs(DIR_LOG, exist_ok=True)
except OSError as e:
    print(e)

try:
    open(os.path.join(DIR_LOG, 'app.log'), 'a').close()

except OSError as e:
    print(e)
