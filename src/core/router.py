import pprint
from functools import wraps

from flask import request, render_template, flash
from urllib.parse import urlparse


class HttpCode:
    OK = 'OK', 200
    Forbidden = 'Forbidden', 403
    Unauthorized = 'Unauthorized', 401


def route(app):

    from core.controllers import perm_controller as perm_ctl, file_controller as file_ctl, group_controller as group_ctl
    from core.db.connector import connectify, sessionify
    from core.logger import logger

    def loggonize(level='debug'):
        def wrapper(func):
            @wraps(func)
            def wrap(*args, **kwargs):
                _request = pprint.pformat(request.environ, depth=5)
                getattr(logger, level)('{} {}'.format(func.__name__, str(_request)))
                return func(*args, **kwargs)
            return wrap
        return wrapper

    @app.route('/', methods=['GET'])
    @loggonize()
    def index():
        return render_template('index.html')

    @app.route('/ping', methods=['GET'])
    @loggonize()
    def ping():
        return 'pong', 200

    @app.route('/test/db', methods=['GET'])
    @loggonize()
    @connectify()
    def test_db(conn):
        res = conn.execute('SELECT 1 AS RES UNION SELECT 2 AS RES')
        msg = ','.join([str(row[0]) for row in res])
        flash(msg)
        return render_template('index.html')

    @app.route('/test/args', methods=['GET'])
    @loggonize()
    def test_args():
        return str(request.args.getlist('id'))

    def _authenticate(session, method, uri, token):
        # check permissions
        is_auth, user = perm_ctl.is_authenticated(session=session, token=token)
        is_avail = perm_ctl.is_action_available(session=session, token=token, method=method, uri=uri)
        is_good = is_auth and is_avail

        # generate result
        if is_good:
            res = HttpCode.OK
        elif is_auth:
            res = HttpCode.Forbidden
        else:
            res = HttpCode.Unauthorized

        # logging authenticate request
        logger.info(
            """AUTH token:'{token}' method:'{method}' uri:'{uri}'
            CHECKS is_auth:{is_auth} is_avail:{is_avail} RESULT {result}""".format(
                result=res, method=method, token=token, uri=uri, is_auth=is_auth, is_avail=is_avail
            ))
        return res, user

    @app.route("/authenticate", methods=['POST'])
    @loggonize()
    @sessionify()
    def authenticate(session):
        # get HEADERs
        method = request.headers.get('X-METHOD', None)
        url = request.headers.get('X-URI', None)
        token = request.headers.get('Authorization', None)

        # get valid (real) uri
        parsed_url = urlparse(url)
        uri = parsed_url.path
        uri = uri.replace(app.config.get('URI_PREFIX', ''), '')

        res, user = _authenticate(session, method, uri, token)

        # do action in DB
        if res == HttpCode.OK:
            if method == 'GET':
                pass
            elif method == 'DELETE':
                file_ctl.remove(session=session, uri=uri)
            elif method == 'PUT':
                groups = None
                # group_names = request.args.getlist('group')
                # groups = group_ctl.check_groups(session, group_names)
                # if type(groups) != list:
                #     return 'Forbidden', 403
                file_ctl.register(session=session, uri=uri, groups=groups, owner_id=user.id, exists_ok=True)
                # file_ctl.patch(session=session, uri=uri, groups=groups, not_exists_ok=True)
        return res

    @app.route("/file/<path:uri>", methods=['PATCH'])
    @loggonize()
    @sessionify()
    def file_patch(session, uri):

        logger.info(
            """FILE PATCH START uri:'{uri}' groups:'{groups}'""".format(
                uri=uri,
                groups=request.args.getlist('group')
            ))

        token = request.headers.get('Authorization', None)
        # get group arg
        group_names = request.args.getlist('group')
        groups = group_ctl.check_groups(session, group_names)
        if type(groups) != list:
            return 'Incorrect value of groups', 400
        # get uri arg
        if not file_ctl.check_file_exists(session, uri):
            return 'Incorrect path - this file does not exists', 400

        res, user = _authenticate(session, 'PATCH', uri, token)

        # do action in DB
        if res == HttpCode.OK:
            file_ctl.patch(session=session, uri=uri, groups=groups)

        # logging authenticate request
        logger.info(
            """FILE PATCH uri:'{uri}' groups: '{groups}' RESULT {res}""".format(
                uri=uri, groups=groups, res=res
            ))

        return res


