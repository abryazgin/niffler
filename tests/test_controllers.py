import unittest

from base import StandartNifflerControllerTest

from core.utils import random_hash
from core.controllers import file_controller, token_controller, group_controller, user_controller
import env


class TestFileController(StandartNifflerControllerTest):
    controller = file_controller
    uri = '{}/{}'.format(random_hash(), random_hash())

    def get_register_kwobj(self, session):
        return {
            'uri': self.uri,
            'owner_id': self.get_test_user().id,
            'groups': [self.get_test_group()]
        }

    def get_remove_kwobj(self, session):
        return {'uri': self.uri}

    def test_remove_not_existing(self):
        self.base_test_remove_ctl(self.session)

    def test_adding_and_removing(self):
        self.base_test_adding_and_removing_ctl(self.session)


class TestTokenController(StandartNifflerControllerTest):
    controller = token_controller
    code = '{}'.format(random_hash())

    def get_register_kwobj(self, session):
        return {'code': self.code, 'user_id': self.get_test_user().id}

    def get_remove_kwobj(self, session):
        return {'code': self.code}

    def test_remove_not_existing(self):
        self.base_test_remove_ctl(self.session)

    def test_adding_and_removing(self):
        self.base_test_adding_and_removing_ctl(self.session)


class TestGroupController(StandartNifflerControllerTest):
    controller = group_controller
    name = '{}'.format(random_hash())

    def get_register_kwobj(self, session):
        return {'name': self.name, 'users': [self.get_test_user()]}

    def get_remove_kwobj(self, session):
        return {'name': self.name}

    def test_remove_not_existing(self):
        self.base_test_remove_ctl(self.session)

    def test_adding_and_removing(self):
        self.base_test_adding_and_removing_ctl(self.session)


class TestUserController(StandartNifflerControllerTest):
    controller = user_controller
    name = '{}'.format(random_hash())

    def get_register_kwobj(self, session):
        return {'name': self.name, 'groups': [self.get_test_group()]}

    def get_remove_kwobj(self, session):
        return {'name': self.name}

    def test_remove_not_existing(self):
        self.base_test_remove_ctl(self.session)

    def test_adding_and_removing(self):
        self.base_test_adding_and_removing_ctl(self.session)


if __name__ == '__main__':
    unittest.main()
