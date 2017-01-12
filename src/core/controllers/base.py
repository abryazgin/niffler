from core.exceptioner import NifflerDBException
from core.logger import logger


def base_register(session, _model, kwobj, exists_ok, _model_name=None, unique_key=None):
    if unique_key is not None:
        kwuniq = {key: kwobj[key] for key in unique_key}
    else:
        kwuniq = kwobj
    if _model_name is None:
        _model_name = _model.__name__
    logger.info('+ Registering {model} {kwobj}'.format(model=_model_name, kwobj=kwobj))
    obj = session.query(_model).filter_by(**kwuniq).one_or_none()
    if not obj:
        logger.info('{model} does not exist. Creating ...'.format(model=_model_name))
        obj = _model(**kwobj)
        session.add(obj)
        session.flush()
    else:
        logger.info('{model} already exist!'.format(model=_model_name))
        if not exists_ok:
            raise NifflerDBException('Current {model} already exists: {obj}'.format(model=_model_name, obj=obj))
    return obj


def base_remove(session, _model, kwobj, not_exists_ok, _model_name=None):
    if _model_name is None:
        _model_name = _model.__name__
    logger.info('- Removing {model} {kwobj}'.format(model=_model_name, kwobj=kwobj))
    obj = session.query(_model).filter_by(**kwobj).one_or_none()
    if obj:
        logger.info('{model} exist. Removing ...'.format(model=_model_name))
        session.delete(obj)
        session.flush()
    else:
        logger.info('{model} not exist yet!'.format(model=_model_name))
        if not not_exists_ok:
            raise NifflerDBException('Current {model} does not exists: {obj}'.format(model=_model_name, obj=obj))
        return False
    return True


def base_patch(session, _model, kwobj, not_exists_ok, _model_name=None, unique_key=None):
    if unique_key is not None:
        kwuniq = {key: kwobj[key] for key in unique_key}
    else:
        kwuniq = kwobj
    if _model_name is None:
        _model_name = _model.__name__
    logger.info('@ Patching {model} {kwobj}'.format(model=_model_name, kwobj=kwobj))
    obj = session.query(_model).filter_by(**kwuniq).one_or_none()
    if obj:
        logger.info('{model} exist. Patching ...'.format(model=_model_name))
        for key in kwobj:
            setattr(obj, key, kwobj[key])
        session.flush()
    else:
        logger.info('{model} not exist yet!'.format(model=_model_name))
        if not not_exists_ok:
            raise NifflerDBException('Current {model} does not exists: {obj}'.format(model=_model_name, obj=obj))
    return obj
