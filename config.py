import logging
import os
from time import strftime

# Statement for enabling the development environment
DEBUG = True
#INFO = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.abspath(os.path.dirname(__file__))+'/../logs'
STATICFILES_DIR = os.path.join('static')


LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
#LOGGING_FILE_NAME = LOG_DIR+'/app/'+strftime('psalm_%Y%d%m%H%M.log')
LOGGING_FILE_NAME = strftime('psalm_%Y%m%d.log')


# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *
#Cross-site Request Forgery (CSRF)* CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

DB_CONNECT = "dynamodb"

logging_config = dict(
    version=1,
    formatters={
        'simple': {'format':'%(levelname)s %(asctime)s { module name : %(module)s Line no : %(lineno)d} %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.handlers.RotatingFileHandler',
              'filename': 'logger.log',
              'maxBytes': 1024 * 1024 * 5,
              'backupCount': 5,
              'level': 'DEBUG',
              'formatter': 'simple',
              'encoding': 'utf8'}
    },

    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)