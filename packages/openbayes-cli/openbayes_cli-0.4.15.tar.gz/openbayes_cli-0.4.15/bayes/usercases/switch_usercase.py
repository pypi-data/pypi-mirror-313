import validators
from bayes.client.status_client import health_check


def is_url(end_point):
    if end_point is not None and end_point != "" and validators.url(end_point):
        return True
    return False


def clean(end_point):
    if end_point.endswith('/'):
        end_point = end_point[:-1]

    return end_point


def is_exist(end_point):
    return health_check(end_point)
