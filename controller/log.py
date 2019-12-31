import logging
from datetime import datetime
from config import DIR_LOG

# logging.basicConfig(filename=DIR_LOG + '/app.log', level=logging.INFO)


def start():
    logging.info(str(__name__)+':<----------------------------' + str(datetime.now()) + '---------------------------->')