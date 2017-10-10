import os
import unittest
from urllib import request

from base import BaseNifflerTest

from core import utils
from core.db import connector


class TestNginx(BaseNifflerTest):

    @staticmethod
    def get_test_url():
        """
        Get open url. For example <domain>:80
        """
        return os.environ['NGINX_TEST_URL']

    @staticmethod
    def get_real_url(uri=''):
        """
        Get private/work url. For example <domain>:8800
        """
        return os.environ['NGINX_REAL_URL'] + '/private' + uri

    def test_environ_vars(self):
        self.assertIsNotNone(os.environ['NGINX_TEST_URL'])
        self.assertIsNotNone(os.environ['NGINX_REAL_URL'])

    def assert_url(self, url, headers=None, method='GET', data=None, res_http_code=200):
        headers = headers if headers else dict()
        # data = data.encode('utf8') if data else None
        _request = request.Request(url=url, headers=headers, method=method, data=data)
        _response = None
        try:
            _response = request.urlopen(_request)
            _code = _response.code
        except Exception as e:
            _code = getattr(e, 'code', None)
            if _code is None:
                print(e)
        self.assertEqual(_code, res_http_code)
        return _response

    """
    TESTS
    """

    def test_config_testing_flag(self):
        self.assertTrue(self.config['TESTING'], 'Test environment')

    def test_urls_exists(self):
        self.assertIsNotNone(TestNginx.get_test_url())
        self.assertIsNotNone(TestNginx.get_real_url())

    @connector.connectify(position=1)
    def test_db_available(self, conn):
        result = conn.execute('SELECT 1').fetchall()[0][0]
        self.assertEqual(result, 1, 'Test DB access')

    # def test_nginx_public_port(self):  # TODO remove this test?
    #     self.assert_url(TestNginx.get_test_url(), res_http_code=200)  # OK

    def test_nginx_private_port_forbidden(self):
        self.assert_url(TestNginx.get_real_url() + '/private', res_http_code=401)  # Unauthorized

    def test_nginx_private_user_case(self):
        file_name = 'test_{}'.format(utils.random_hash())
        uri = '/{}'.format(file_name)
        url = TestNginx.get_real_url(uri)
        headers = {'Authorization': self.test_token.code}
        headers2 = {'Authorization': self.test_token2.code}
        headers3 = {'Authorization': self.test_token3.code}
        data = b'some text'
        data2 = b'some text2'
        # getting not existing file
        self.assert_url(url=url, headers=headers, method='GET', res_http_code=403)  # Forbidden
        # putting file
        self.assert_url(url=url, headers=headers, method='PUT', data=data, res_http_code=201)  # Created
        # getting existing file + check body
        result = self.assert_url(url=url, headers=headers, method='GET', res_http_code=200)  # OK
        self.assertEqual(result.read(), data)
        # others users
        self.assert_url(url=url, headers=headers2, method='GET', res_http_code=403)  # Forbidden
        self.assert_url(url=url, headers=headers3, method='GET', res_http_code=403)  # Forbidden
        # patch - add access to group
        self.assert_url(url=url + '?group=' + self.test_group.name, headers=headers, method='PATCH', res_http_code=200)  # OK
        # others users
        self.assert_url(url=url, headers=headers2, method='GET', res_http_code=200)  # OK
        self.assert_url(url=url, headers=headers3, method='GET', res_http_code=403)  # Forbidden
        # re-putting file
        self.assert_url(url=url, headers=headers, method='PUT', data=data2, res_http_code=204)  # No Content
        # getting new file + check that body has been changed
        result = self.assert_url(url=url, headers=headers, method='GET', res_http_code=200)  # OK
        self.assertEqual(result.read(), data2)
        # delete existing file
        self.assert_url(url=url, headers=headers, method='DELETE', res_http_code=204)  # No Content
        # delete not existing file
        self.assert_url(url=url, headers=headers, method='DELETE', res_http_code=403)  # Forbidden

if __name__ == '__main__':
    unittest.main()
