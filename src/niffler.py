from flask import Flask
import logging

from core.router import route
app = Flask(__name__)

app.config.from_envvar('CONFIG_PATH')
app.debug = app.config.get('DEBUG', False)
app.secret_key = '6048ba310f595ad189c5fa7c2666e9f1e1cc99dff66da4c1'
app.logger.setLevel(app.config.get('LOGGER_LEVEL', logging.INFO))


from core.eventer import prerun
prerun()
route(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
