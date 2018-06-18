#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
# Run a test server.
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from logging.config import dictConfig

from config import logging_config
#from app import app
#from app.routes.church import *
from app.routes.index import *
from app.routes.user import *
from app.routes.church import *
from app.routes.procedure import *
from app.routes.score import *
#app = Flask('psalm')

#logger = logging.getLogger('psalmLog')
app.config.from_object('config')
app.logger.info(app.config["BASE_DIR"])

logger = app.logger
logger.setLevel(app.config["LOGGING_LEVEL"])

#handler = RotatingFileHandler(app.config["BASE_DIR"] + '../logs/app/' + app.config["LOGGING_FILE_NAME"],maxBytes=1024*1024*500, backupCount=3)
handler = RotatingFileHandler(app.config["LOGGING_FILE_NAME"],maxBytes=1024*1024*500, backupCount=3)
handler.setLevel(app.config["LOGGING_LEVEL"])
handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
logger.addHandler(handler)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(app.config["LOGGING_LEVEL"])
streamHandler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
logger.addHandler(streamHandler)

#dictConfig(logging_config)

if __name__ == '__main__':
    app.run()
    # # app.logger.debug('test'+__name__)
    # # app.logger.debug('testdddddddddddd')
    # # print (__name__)
    # # print (app.root_path)
    # # print (app.import_name)
    # #logger = logging.getLogger('psalmLog')
    # logger = app.logger
    # logger.setLevel(logging.DEBUG)
    # handler = RotatingFileHandler(app.config["BASE_DIR"]+'/'+app.config["LOGGING_FILE_NAME"], maxBytes=7000, backupCount=3)
    # handler.setLevel(app.config["LOGGING_LEVEL"])
    # handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
    # logger.addHandler(handler)
    # #
    # # #formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # # #handler.setFormatter(formatter)
    # #
    # streamHandler = logging.StreamHandler()
    # streamHandler.setLevel(logging.DEBUG)
    # streamHandler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
    # logger.addHandler(streamHandler)
    #
    # #
    # # app.logger.setLevel(app.config["LOGGING_LEVEL"])
    # # app.logger.addHandler(handler)
    # # app.logger.addHandler(streamHandler)
    # # app.logger.info('info log start!')
    # #
    # #
    # # log = logging.getLogger()
    # # log.setLevel(logging.ERROR)
    # # log.addHandler(handler)
    #
    # #app.config["DEBUG"] = app.config["DEBUG"]
    #
    #
    # #app.run(host='0.0.0.0', debug=True)
    # #dictConfig(logging_config)
    #
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')