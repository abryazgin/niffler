from core.db.models import Token
from core.controllers.base import base_register, base_remove

_model = Token


def register(session, code, user_id, exists_ok=False):
    kwobj = {'code': code, 'user_id': user_id}
    unique_key = ['code']
    return base_register(session, _model=_model, kwobj=kwobj, exists_ok=exists_ok, unique_key=unique_key)


def remove(session, code, not_exists_ok=False):
    kwobj = {'code': code}
    return base_remove(session, _model=_model, kwobj=kwobj, not_exists_ok=not_exists_ok)
