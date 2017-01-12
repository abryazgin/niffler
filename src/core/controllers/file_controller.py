from core.db.models import File
from core.controllers.base import base_register, base_remove, base_patch

_model = File


def register(session, uri, owner_id, groups=None, exists_ok=False):
    kwobj = {'uri': uri, 'owner_id': owner_id}
    if groups:
        kwobj['groups'] = groups
    unique_key = ['uri']
    return base_register(session, _model=_model, kwobj=kwobj, exists_ok=exists_ok, unique_key=unique_key)


def remove(session, uri, not_exists_ok=False):
    kwobj = {'uri': uri}
    return base_remove(session, _model=_model, kwobj=kwobj, not_exists_ok=not_exists_ok)


def patch(session, uri, groups, not_exists_ok=False):
    kwobj = {'uri': uri, 'groups': groups}
    unique_key = ['uri']
    return base_patch(session, _model=_model, kwobj=kwobj, not_exists_ok=not_exists_ok, unique_key=unique_key)


def check_file_exists(session, uri):
    return File.is_exists(session, uri)
