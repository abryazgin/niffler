import unittest

from base import BaseNifflerTest
import env

from core import utils
from core.controllers import perm_controller
from core.db import connector
from core.db.models import User


class TestNiffler(BaseNifflerTest):

    def test_config_testing_flag(self):
        self.assertTrue(self.config['TESTING'], 'Test environment')

    @connector.connectify(position=1)
    def test_db_available(self, conn):
        result = conn.execute('SELECT 1').fetchall()[0][0]
        self.assertEqual(result, 1, 'Test DB access')

    def test_testuser_is_authenticated(self):
        self.assertTrue(perm_controller.is_authenticated(session=self.session, token=self.test_token.code))
        self.assertTrue(perm_controller.is_authenticated(session=self.session, token=self.test_token2.code))
        self.assertTrue(perm_controller.is_authenticated(session=self.session, token=self.test_token3.code))

    def test_random_is_not_authenticated(self):
        # check that doesn't exists some random tokens
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token=utils.random_hash())[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token=utils.random_hash())[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token=utils.random_hash())[0])
        # check that doesn't exists simplest tokens
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='1')[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='11')[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='111')[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='asd')[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='qwe')[0])
        self.assertFalse(perm_controller.is_authenticated(session=self.session, token='qwerty')[0])

    def test_is_action_available(self):
        uri = self.test_file.uri
        token = self.test_token.code
        token2 = self.test_token2.code
        token3 = self.test_token3.code
        self.assertTrue(perm_controller.is_action_available(session=self.session, uri=uri, token=token, method='DELETE'))
        self.assertTrue(perm_controller.is_action_available(session=self.session, uri=uri, token=token, method='GET'))
        self.assertTrue(perm_controller.is_action_available(session=self.session, uri=uri, token=token, method='PUT'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token, method='MOVE'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token, method='POST'))

        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token2, method='DELETE'))
        self.assertTrue(perm_controller.is_action_available(session=self.session, uri=uri, token=token2, method='GET'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token2, method='PUT'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token2, method='MOVE'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token2, method='POST'))

        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token3, method='DELETE'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token3, method='GET'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token3, method='PUT'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token3, method='MOVE'))
        self.assertFalse(perm_controller.is_action_available(session=self.session, uri=uri, token=token3, method='POST'))

    def test_users_exists(self):
        count = self.session.query(User).count()
        self.assertTrue(count > 0, 'Some users must exists')


if __name__ == '__main__':
    unittest.main()
