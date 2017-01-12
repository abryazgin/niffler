import os

from niffler import app
from core.controllers import file_controller, user_controller, group_controller, token_controller
from core import utils


def get_test_env():
    return {
        'user': {
            'name': 'test_user1_{}'.format(utils.random_hash(7)),
        },
        'token': {
            'code': 'test_token1_{}'.format(utils.random_hash(7))
        },
        'user2': {
            'name': 'test_user2_{}'.format(utils.random_hash(7)),
        },
        'token2': {
            'code': 'test_token2_{}'.format(utils.random_hash(7))
        },
        'user3': {
            'name': 'test_user3_{}'.format(utils.random_hash(7)),
        },
        'token3': {
            'code': 'test_token3_{}'.format(utils.random_hash(7))
        },
        'group': {
            'name': 'test_group_{}'.format(utils.random_hash(7)),
        },
        'file': {
            'uri': 'test/test_file_{}.ext'.format(utils.random_hash(7)),
        },
        'file_content': 'some text for test file'
    }
'''
TOKEN  ----->> USER <<-----------------`owner`
                                            |
TOKEN2 ----->> USER2 ---->> GROUP <<---->> FILE

TOKEN3 ----->> USER3
'''


def create_test_user_if_note_exists(session, test, user_key='user'):
    obj = test.get(user_key)
    return user_controller.register(session, exists_ok=True, **obj)


def create_test_group_if_note_exists(session, test):
    user = create_test_user_if_note_exists(session, test, 'user2')
    create_test_token_if_note_exists(session, test, token_key='token2', user_key='user2')
    obj = {
        'name': test.get('group').get('name'),
        'users': [user]
    }
    return group_controller.register(session, exists_ok=True, **obj)


def create_test_token_if_note_exists(session, test, token_key='token', user_key='user'):
    user = create_test_user_if_note_exists(session, test, user_key)
    obj = {
        'user_id': user.id,
        'code': test.get(token_key).get('code')
    }
    return token_controller.register(session, exists_ok=True, **obj)


def create_test_file_if_note_exists(session, test):
    # create file physically in OS
    uri = test.get('file').get('uri')
    file_path = os.path.join(app.config['FILE_ROOT'], 'private', uri)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(test.get('file_content'))

    # create file in DB
    user = create_test_user_if_note_exists(session, test)
    group = create_test_group_if_note_exists(session, test)
    file = file_controller.register(session, owner_id=user.id, groups=[group], uri=uri, exists_ok=True)
    return file


def remove_test_file_if_note_exists(session, test):
    # remove file physically from OS
    uri = test.get('file').get('uri')
    file_path = os.path.join(app.config['FILE_ROOT'], 'private', uri)
    os.remove(file_path)

    # remove file from DB
    file = file_controller.remove(session, uri=uri)
    return file
