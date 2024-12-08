import requests


def request_dtr(route):
    """
    Request an API of a datatype registry to get information about a schema
    :param route: a path for requesting a dtr API
    :return: requested information about the schema
    """
    r = requests.get(route)
    return r.json()
