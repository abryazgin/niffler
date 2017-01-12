import uuid


def random_hash(length=None):
    return uuid.uuid4().hex[:length]
