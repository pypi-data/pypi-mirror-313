import concurrent.futures
from http import HTTPStatus
import json
import logging
import time

from furl import furl

from .constants import VINZ_URL, DEFAULT_POLLING_TIMEOUT, POLLING_INTERVAL
from .requests import get_session
from .response import validate_response
from .utils import progress

logger = logging.getLogger(__name__)


def _get_headers(access_token):
    return {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }

def _add_params(f, params=None):
    if params is None:
        params = {}

    for k, v in params.items():
        if v:
            f.args[k] = v
    return f

def _process_data(data):
    if not data:
        return '{}'
    return json.dumps({k: v for k, v in data.items() if v is not None})

def _paginate(method, url, access_token, params=None):
    results = []
    if params is None:
        params = {}
    if params.get('limit') is None:
        params['limit'] = 100

    if params.get('offset') is None:
        params['offset'] = 0

    def _get_results(_url, _params):
        f = furl(_url)
        f = _add_params(f, _params)
        _response = session.request(method, f.url, headers=_get_headers(access_token))
        _response.raise_for_status()
        return _response

    session = get_session()
    while True:
        response = _get_results(url, params)
        data = response.json()
        if not data:
            break

        results.extend(data)

        if len(data) < params['limit']:
            break
        params['offset'] = params['offset'] + params['limit']
    return results

@progress('Retrieving...')
def _get(access_token, resource, _id=None, method='get', params=None):
    session = get_session()

    f = furl(VINZ_URL)
    f.path = f'api/{resource}/{_id}' if _id else f'api/{resource}'
    f = _add_params(f, params)
    url = f.url

    response = session.request(method, url, headers=_get_headers(access_token))
    validate_response(response)
    return response.status_code, response.json()

@progress('Retrieving...')
def _list(access_token, resource, method='get', params=None, is_paginated=True):
    session = get_session()

    f = furl(VINZ_URL)
    f.path = f'api/{resource}'
    url = f.url

    # return all the records if limit not specified
    if is_paginated and not params.get('limit') and not params.get('offset'):
        return 200, _paginate(method, url, access_token, params)

    f = _add_params(f, params)
    url = f.url
    response = session.request(method, url, headers=_get_headers(access_token))
    validate_response(response)
    return response.status_code, response.json()

@progress('Creating...')
def _create(access_token, resource, method='put', data=None, params=None):
    session = get_session()

    f = furl(VINZ_URL)
    f.path = f'api/{resource}'
    f = _add_params(f, params)

    url = f.url
    data = _process_data(data)

    response = session.request(method, url, headers=_get_headers(access_token), data=data)
    validate_response(response)
    if response.status_code == HTTPStatus.NO_CONTENT:
        return response.status_code, None
    elif response.status_code == HTTPStatus.ACCEPTED:
        return response.status_code, response.headers['Location']
    else:
        return response.status_code, response.json()

@progress('Updating...')
def _update(access_token, resource, method='patch', data=None, params=None):
    session = get_session()

    f = furl(VINZ_URL)
    f.path = f'api/{resource}'
    f = _add_params(f, params)

    url = f.url
    data = _process_data(data)

    response = session.request(method, url, headers=_get_headers(access_token), data=data)
    validate_response(response)
    if response.status_code == HTTPStatus.NO_CONTENT:
        return response.status_code, None
    elif response.status_code == HTTPStatus.ACCEPTED:
        return response.status_code, response.headers['Location']
    else:
        return response.status_code, response.json()

@progress('Deleting...')
def _delete(access_token, resource, method='delete', data=None, params=None):
    session = get_session()

    f = furl(VINZ_URL)
    f.path = f'api/{resource}'
    f = _add_params(f, params)

    url = f.url
    if data:
        response = session.request(method, url, headers=_get_headers(access_token), data=_process_data(data))
    else:
        response = session.request(method, url, headers=_get_headers(access_token))

    validate_response(response)
    if response.status_code != HTTPStatus.NO_CONTENT:
        return response.status_code, response.json()
    return response.status_code, None

@progress(message='Polling results...')
def _poll_response(access_token, job_id, path='job', timeout=DEFAULT_POLLING_TIMEOUT):
    def poll(_url):
        while True:
            session = get_session()
            _response = session.get(_url, headers=_get_headers(access_token))
            validate_response(_response)

            data = _response.json()
            status = data.get("status")
            if status != "InProgress":
                return data

            time.sleep(POLLING_INTERVAL)

    def poll_until_finished(_url):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(poll, _url)
            try:
                done, _ = concurrent.futures.wait([future], timeout=timeout)
                for f in done:
                    return f.result()
            except concurrent.futures.TimeoutError:
                future.cancel()
                raise Exception("Polling timeout")
            except Exception as e:
                logger.error(f"Polling failed: {e}")
                raise e

    url = f"{VINZ_URL}/api/{path}/{job_id}"

    response = poll_until_finished(url)
    return response
