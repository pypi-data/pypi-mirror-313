"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: HttpRequest.py
@Time: 2023/12/9 18:00
"""

import json as json_v2
from urllib import parse
from urllib.parse import unquote

from requests import Response
from requests import Session

from SteamedBread import logger


def __hook_response(response: Response, **kwargs):
    try:
        result = json_v2.dumps(response.json(), ensure_ascii=False)
    except Exception as e:
        result = response.text or e

    kwargs = {"服务code码": response.status_code, **kwargs}
    query = unquote(parse.urlparse(response.url).query or parse.urlparse(response.url).params)

    logger.info(f"""
    请求方法: {response.request.method}
    请求地址: {response.request.url.split("?")[0]}
    请求内容: {response.request.body or query or {} }
    请求响应: {result}
    请求时长: {response.elapsed.total_seconds()} 秒
    更多内容: {kwargs}
        """)


def request(url,
            method="post",
            show=True,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            timeout=10,
            verify=None,
            json=None,
            **kwargs):
    """

    :param url:
    :param method:
    :param show:
    :param params:
    :param data:
    :param headers:
    :param cookies:
    :param timeout:
    :param verify:
    :param json:
    :param kwargs:
    :return:
    """
    show = kwargs.get("show") or show
    with Session() as session:
        return session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            verify=verify,
            json=json,
            hooks=dict(response=__hook_response) if show else None,
            **kwargs)


def get(url, show=True, params=None, headers=None, cookies=None, timeout=10, verify=None, **kwargs):
    r"""Sends a GET request.

    :param show:
    :param verify:
    :param timeout:
    :param cookies:
    :param headers:
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="get",
                   url=url,
                   show=show,
                   params=params,
                   headers=headers,
                   cookies=cookies,
                   timeout=timeout,
                   verify=verify, **kwargs)


def options(url, **kwargs):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="options", url=url, **kwargs)


def head(url, **kwargs):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    kwargs.setdefault("allow_redirects", False)
    return request(method="head", url=url, **kwargs)


def post(url,
         data=None,
         show=True,
         params=None,
         json=None,
         headers=None,
         cookies=None,
         timeout=10,
         verify=None,
         **kwargs):
    r"""Sends a POST request.

    :param show:
    :param verify:
    :param timeout:
    :param params:
    :param cookies:
    :param headers:
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="post",
                   url=url,
                   show=show,
                   data=data,
                   json=json,
                   params=params,
                   headers=headers,
                   cookies=cookies,
                   timeout=timeout,
                   verify=verify,
                   **kwargs)


def put(url,
        data=None,
        show=True,
        params=None,
        json=None,
        headers=None,
        cookies=None,
        timeout=10,
        verify=None,
        **kwargs):
    r"""Sends a PUT request.

    :param data:
    :param show:
    :param params:
    :param json:
    :param verify:
    :param timeout:
    :param cookies:
    :param headers:
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="put",
                   url=url,
                   show=show,
                   data=data,
                   json=json,
                   params=params,
                   headers=headers,
                   cookies=cookies,
                   timeout=timeout,
                   verify=verify,
                   **kwargs)


def patch(url, data=None, **kwargs):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="patch", url=url, data=data, **kwargs)


def delete(url,
           data=None,
           show=True,
           params=None,
           json=None,
           headers=None,
           cookies=None,
           timeout=10,
           verify=None,
           **kwargs):
    r"""Sends a DELETE request.

    :param data:
    :param show:
    :param params:
    :param json:
    :param verify:
    :param timeout:
    :param cookies:
    :param headers:
    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request(method="delete",
                   url=url,
                   show=show,
                   data=data,
                   json=json,
                   params=params,
                   headers=headers,
                   cookies=cookies,
                   timeout=timeout,
                   verify=verify,
                   **kwargs)
