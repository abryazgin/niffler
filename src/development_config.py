import logging
import os

from niffler import app

DATABASE_URL = '/'.join(('sqlite://', app.root_path, '..', 'development.db'))
DEBUG = True
FILE_ROOT = '/tmp/niffler'
LOGGER_LEVEL = logging.DEBUG
LOGGER_FILE_PATH = os.path.join(app.root_path, 'flask.log')
