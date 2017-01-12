import unittest

from core import utils

from base import BaseNifflerTest
import env


class TestNiffler(BaseNifflerTest):
    def test_test_db(self):
        rv = self.app.get('/test/db')
        assert b'1,2' in rv.data

    def check_authenticate(self, token, code, method, uri):
        rv = self.app.post('/authenticate', headers={'Authorization': token, 'X-METHOD': method, 'X-URI': uri})
        self.assertTrue(str(code) in rv.status, 'Incorrect result code: rec {} req {}'.format(rv.status, code))

    def test_authenticate_GET_PUT_DELETE_others(self):
        uri = utils.random_hash()
        token = self.test_token.code
        token2 = self.test_token2.code
        token3 = self.test_token3.code
        token4 = utils.random_hash()
        self.check_authenticate(code=403, uri=uri, token=token, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token, method='PUT')
        self.check_authenticate(code=200, uri=uri, token=token, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token, method='MOVE')
        self.check_authenticate(code=403, uri=uri, token=token, method='POST')
        self.check_authenticate(code=200, uri=uri, token=token, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token, method='DELETE')

        self.check_authenticate(code=403, uri=uri, token=token2, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token2, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token2, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token2, method='PUT')
        self.check_authenticate(code=200, uri=uri, token=token2, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token2, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token2, method='MOVE')
        self.check_authenticate(code=403, uri=uri, token=token2, method='POST')
        self.check_authenticate(code=200, uri=uri, token=token2, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token2, method='DELETE')

        self.check_authenticate(code=403, uri=uri, token=token3, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token3, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token3, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token3, method='PUT')
        self.check_authenticate(code=200, uri=uri, token=token3, method='PATCH')
        self.check_authenticate(code=200, uri=uri, token=token3, method='GET')
        self.check_authenticate(code=403, uri=uri, token=token3, method='MOVE')
        self.check_authenticate(code=403, uri=uri, token=token3, method='POST')
        self.check_authenticate(code=200, uri=uri, token=token3, method='DELETE')
        self.check_authenticate(code=403, uri=uri, token=token3, method='DELETE')

        self.check_authenticate(code=401, uri=uri, token=token4, method='DELETE')
        self.check_authenticate(code=401, uri=uri, token=token4, method='GET')
        self.check_authenticate(code=401, uri=uri, token=token4, method='PATCH')
        self.check_authenticate(code=401, uri=uri, token=token4, method='PUT')
        self.check_authenticate(code=401, uri=uri, token=token4, method='MOVE')
        self.check_authenticate(code=401, uri=uri, token=token4, method='POST')


if __name__ == '__main__':
    unittest.main()
