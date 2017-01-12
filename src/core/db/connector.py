from functools import wraps

from core.db.base import engine, Session


def connectify(position=0):
    """
    DB connection wrapper

    :param position: position in args of wrapped function to insert connection parameter
    """
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            conn = None
            trans = None
            try:
                conn = engine.connect()
                trans = conn.begin()

                args = list(args)
                args[position:position] = [conn]
                result = func(*args, **kwargs)

                trans.commit()
                return result
            except:
                if trans:
                    trans.rollback()
                raise
            finally:
                if conn:
                    conn.close()
        return wrap
    return wrapper


def sessionify(position=0):
    """
    DB session wrapper

    :param position: position in args of wrapped function to insert session parameter
    """
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            session = None
            try:
                session = Session()

                args = list(args)
                args[position:position] = [session]
                result = func(*args, **kwargs)

                session.commit()
                return result
            except:
                if session:
                    session.rollback()
                raise
            finally:
                if session:
                    session.close()
        return wrap
    return wrapper


def get_session():
    return Session()


