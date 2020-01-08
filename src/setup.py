import logging
import logging.config
import os
import json



BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mylogger():
    logging.config.fileConfig(os.path.join(BASE_DIR,"conf","logging.ini"))
    # get an instance of the logger object this module will use
    mylogger = logging.getLogger(__name__)
    return mylogger

LOGGER = mylogger()
INFO = LOGGER.info
DEBUG = LOGGER.debug
ERROR = LOGGER.error

def mycredsfile():
    credsfile = os.path.join(BASE_DIR, "my.creds")
    creds = json.loads(open(credsfile).read())
    return creds

CREDS = mycredsfile()
