import unittest

import niffler
from core.db.connector import get_session
from core.exceptioner import NifflerDBException

import env


class BaseNifflerTest(unittest.TestCase):

    def setUp(self):
        niffler.app.config['TESTING'] = True
        self.app = niffler.app.test_client()
        self.config = niffler.app.config

        self.init_test_venv()

    def tearDown(self):
        self.clear_test_venv()
        self.session.close()

    def init_test_venv(self):
        self.session = get_session()
        self.test_env = env.get_test_env()
        self.test_user = env.create_test_user_if_note_exists(self.session, self.test_env)
        self.session.commit()
        self.test_user2 = env.create_test_user_if_note_exists(self.session, self.test_env, 'user2')
        self.session.commit()
        self.test_user3 = env.create_test_user_if_note_exists(self.session, self.test_env, 'user3')
        self.session.commit()
        self.test_token = env.create_test_token_if_note_exists(self.session, self.test_env)
        self.session.commit()
        self.test_token2 = env.create_test_token_if_note_exists(self.session, self.test_env, token_key='token2', user_key='user2')
        self.session.commit()
        self.test_token3 = env.create_test_token_if_note_exists(self.session, self.test_env, token_key='token3', user_key='user3')
        self.session.commit()
        self.test_group = env.create_test_group_if_note_exists(self.session, self.test_env)
        self.session.commit()
        self.test_file = env.create_test_file_if_note_exists(self.session, self.test_env)
        self.session.commit()

    def clear_test_venv(self):
        env.remove_test_file_if_note_exists(self.session, self.test_env)
        self.session.commit()
        self.session.delete(self.test_token)
        self.session.commit()
        self.session.delete(self.test_token2)
        self.session.commit()
        self.session.delete(self.test_token3)
        self.session.commit()
        self.session.delete(self.test_user)
        self.session.commit()
        self.session.delete(self.test_user2)
        self.session.commit()
        self.session.delete(self.test_user3)
        self.session.commit()
        self.session.delete(self.test_group)
        self.session.commit()
        self.session.close()

    def get_test_user(self):
        return self.test_user

    def get_test_group(self):
        return self.test_group

    def get_test_token(self):
        return self.test_token

    def get_test_file(self):
        return self.test_file


class StandartNifflerControllerTest(BaseNifflerTest):

    controller = None

    def get_remove_kwobj(self, session):
        raise NotImplementedError()

    def get_register_kwobj(self, session):
        raise NotImplementedError()

    def base_test_remove_ctl(self, session):
        remove_kwobj = self.get_remove_kwobj(session)
        # not exists - check exception ( + check default not_exists_ok = False)
        with self.assertRaises(NifflerDBException):
            self.controller.remove(session, **remove_kwobj)
        # not exists - check exception
        with self.assertRaises(NifflerDBException):
            self.controller.remove(session, not_exists_ok=False, **remove_kwobj)
        # not exists - check NOT exception
        self.assertFalse(self.controller.remove(session, not_exists_ok=True, **remove_kwobj))
        session.commit()

    def base_test_adding_and_removing_ctl(self, session):
        remove_kwobj = self.get_remove_kwobj(session)
        register_kwobj = self.get_register_kwobj(session)
        # exists - check exception ( + check default exists_ok = False)
        obj = self.controller.register(session, **register_kwobj)
        self.assertIsNotNone(obj)
        with self.assertRaises(NifflerDBException):
            self.controller.register(session, **register_kwobj)
        # exists - check exception
        with self.assertRaises(NifflerDBException):
            self.controller.register(session, exists_ok=False, **register_kwobj)
        # check duplicate inserting
        self.assertEqual(self.controller.register(session, exists_ok=True, **register_kwobj), obj)
        # check inserted object
        for key in register_kwobj:
            self.assertEqual(register_kwobj.get(key), getattr(obj, key))
        # check delete returned file
        self.assertTrue(self.controller.remove(session, **remove_kwobj))
        # check delete by exists_ok=True, not_exists_ok=True
        obj = self.controller.register(session, exists_ok=True, **register_kwobj)
        self.assertIsNotNone(obj)
        self.assertTrue(self.controller.remove(session, not_exists_ok=True, **remove_kwobj))


if __name__ == '__main__':
    unittest.main()
