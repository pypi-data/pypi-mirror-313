import requests
from requests.exceptions import HTTPError

from anylearn.sdk.auth import configure_auth
from anylearn.sdk.utils import RequestRetrySession, raise_for_status


def request(method, *args, **kwargs):
    with RequestRetrySession() as sess:
        res = sess.request(method, *args, **kwargs)
        raise_for_status(res)
        res.encoding = "utf-8"
        return res.json()


def request_with_token(method, *args, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    auth = configure_auth()
    kwargs['headers']['Authorization'] = f"Bearer {auth.access_token}"
    try:
        return request(method, *args, **kwargs)
    except HTTPError as e:
        if e.response.status_code == 401 and auth.refresh_token:
            auth = configure_auth(force=True)
            if auth:
                return request_with_token(method, *args, **kwargs)
        raise


def get_with_token(*args, **kwargs):
    return request_with_token('GET', *args, **kwargs)


def post_with_token(*args, **kwargs):
    return request_with_token('POST', *args, **kwargs)


def delete_with_token(*args, **kwargs):
    return request_with_token('DELETE', *args, **kwargs)


def put_with_token(*args, **kwargs):
    return request_with_token('PUT', *args, **kwargs)


def patch_with_token(*args, **kwargs):
    return request_with_token('PATCH', *args, **kwargs)
