from core.db.models import User, Role
from core.controllers.base import base_register, base_remove

_model = User


def register(session, name, groups=None, exists_ok=False):
    kwobj = {'name': name, 'role_id': Role.CLIENT}
    if groups:
        kwobj['groups'] = groups
    unique_key = ['name']
    return base_register(session, _model=_model, kwobj=kwobj, exists_ok=exists_ok, unique_key=unique_key)


def remove(session, name, not_exists_ok=False):
    kwobj = {'name': name}
    return base_remove(session, _model=_model, kwobj=kwobj, not_exists_ok=not_exists_ok)


def get_by_token(session, token):
    return User.get_by_token(session=session, token=token)
