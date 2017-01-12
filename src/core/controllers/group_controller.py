from core.db.models import Group
from core.controllers.base import base_register, base_remove

_model = Group


def register(session, name, users=None, exists_ok=False):
    kwobj = {'name': name}
    if users:
        kwobj['users'] = users
    unique_key = ['name']
    return base_register(session, _model=_model, kwobj=kwobj, exists_ok=exists_ok, unique_key=unique_key)


def remove(session, name, not_exists_ok=False):
    kwobj = {'name': name}
    return base_remove(session, _model=_model, kwobj=kwobj, not_exists_ok=not_exists_ok)


def check_groups(session, group_names):
    groups = []
    for group_name in group_names:
        group = Group.get_by_name(session, group_name)
        if not group:
            return False
        groups.append(group)
    return groups
