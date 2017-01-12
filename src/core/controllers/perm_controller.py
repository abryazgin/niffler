from core.exceptioner import NifflerException
from core.db.connector import sessionify
from core.db.models import User, File


def is_authenticated(session, token):
    user = User.get_by_token(session, token)
    return user is not None, user


def is_action_available(session, token, method, uri):
    """
    Check if action available. Checking by:

    :param session: ORM session
    :param token: token for authentication user
    :param method: method (GET, POST, DELETE, etc.)
    :param uri: uri of file (for example `/test/some/file.txt`)
    :return:

    Rules:

    If file exist:
     ---------------------------------------------------
    |            | GET | PUT | DELETE | PATCH | others  |
    |---------------------------------------------------|
    | for owner  |  +  |  +  |   +    |   +   |    -    |
    | for group  |  +  |  -  |   -    |   -   |    -    |
    | for others |  -  |  -  |   -    |   -   |    -    |
     ---------------------------------------------------
    If file NOT exist:
                  --------------------------------------
                 | GET | PUT | DELETE | PATCH | others  |
                 |--------------------------------------|
                 |  -  |  +  |   -    |   -   |    -    |
                  --------------------------------------
    """
    if method not in ('GET', 'PUT', 'DELETE', 'PATCH'):
        return False
    # If file exist:
    if File.is_exists(session=session, uri=uri):
        # for owner
        if File.is_token_of_owner(session=session, uri=uri, token=token):
            return True
        # for group
        elif File.is_token_of_accessed_group(session=session, uri=uri, token=token):
            if method == 'GET':
                return True
            else:
                return False
        # for others
        else:
            return False
    # If file NOT exist:
    else:
        if method == 'PUT':
            return True
        else:
            return False
