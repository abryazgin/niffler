from niffler import app


logger = app.logger


def init():
    import logging
    file_path = app.config.get('LOGGER_FILE_PATH', None)
    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(app.config.get('LOGGER_LEVEL', logging.INFO))
        app.logger.addHandler(file_handler)

