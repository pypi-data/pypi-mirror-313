from typing import TypedDict
import urllib.parse
from http.client import HTTPConnection, HTTPResponse
from json import dumps, loads
from logging import Logger

from requests import JSONDecodeError, Session, Response
from urllib3.filepost import choose_boundary

from lljz_tools import logger
from lljz_tools.c_random import random_string
from lljz_tools.color import Color
from lljz_tools.decorators import thread_lock, debug


class URL(str):
    def __init__(self, __url: str, /):
        assert isinstance(__url, str), f'{type(__url)} is not str!'
        __url = __url.strip()
        if __url:
            assert __url.startswith('http://') or __url.startswith('https://'), 'url必须以http://或https://开头'
        if __url.endswith('/'):
            print(Color.yellow("url请不要带有‘/’结尾"))
            __url = __url[:-1]
        self._url = __url

    def __str__(self):
        return self._url

    def __repr__(self):
        return self._url

    @property
    def url(self):
        return self._url


class HTTPClient(Session):

    def __init__(self, base_url: URL | str = '', *, timeout=120, debug: bool | Logger = False):
        super().__init__()
        url = base_url if isinstance(base_url, URL) else URL(base_url)
        self._base_url = url.url
        self._timeout = timeout
        self.debug = bool(debug)
        self._logger = debug if isinstance(debug, Logger) else logger
        self._response: Response | None = None
        self.key: str | int = random_string(10)

    def login(self, *args, **kwargs):
        raise NotImplementedError('登录接口尚未实现，建议获取到token后，将token等信息添加到self.headers中')

    def get_response_data(self, status_code=200, *, message_key='message', data_key='data', **kwargs):
        if self._response is None:
            raise ValueError('响应数据为空！')
        try:
            data = self._response.json()
        except JSONDecodeError:
            assert self._response.status_code == status_code, \
                (f'请求失败，预期[{status_code}]、实际[{self._response.status_code}]。'
                 f'响应结果为：{self._response.text[:200]}')
        else:
            if message_key not in data:
                self._logger.warning(f"响应数据中缺少“{message_key=}”字段，请重新设置message_key字段")
                message = data
            else:
                message = data[message_key]
            assert self._response.status_code == status_code, \
                f'请求失败，预期[{status_code}]、实际[{self._response.status_code}]。提示：{message[:200]}'
            for key, value in kwargs.items():
                if key not in data:
                    raise KeyError(f'响应数据缺少{key}字段')
                assert data[key] == value, \
                    f'响应数据[{key}]值不匹配，预期[{value}]、实际[{data[key]}](提示信息：{message})'
            if data_key not in data:
                self._logger.warning(f"响应数据中缺少“{data_key=}”字段，请重新设置data_key字段")
                return data
            return data[data_key]

    check_response = get_response_data

    def __hiddenKey(self, data, hiddenKey: str):
        if not isinstance(data, dict):
            return data
        return {k: '******' if isinstance(k, str) and k.upper() == hiddenKey.upper() else v for k, v in data.items()}

    def request(
            self,
            method,
            url: str | bytes,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=False,
            cert=None,
            json=None,
    ):
        run_url = self._base_url + str(url)
        if self.debug:
            method = str(method.upper())
            method_color_factory = {
                'POST': Color.yellow, 
                'GET': Color.green, 
                'DELETE': Color.red, 
                'PUT': Color.magenta
            }   
            method_color = method_color_factory.get(method, Color.cyan)  
            self._logger.info(f'{method_color(method)} - {run_url}', stacklevel=5)
        if self.debug and params:
            self._logger.info(f'params - {self.__hiddenKey(params, 'password')}', stacklevel=5)
        if self.debug and json:
            try:
                json_data = dumps(self.__hiddenKey(json, 'password'), ensure_ascii=False)
                self._logger.info(f'Payload - {json_data}', stacklevel=5)
            except TypeError as e:
                self._logger.error(f'json dumps error: {e}', stacklevel=5)
        if self.debug and data:
            self._logger.info(f'Form data - {data}', stacklevel=5)

        response = super().request(
            method, run_url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )
        self._response = response
        return response


class FastResponse:

    def __init__(self, response: HTTPResponse):
        self._response = response
        self.status_code = response.status
        self.content = response.read()
        self.text = self.content.decode('utf-8')
        self.headers = response.headers
        self._json = None

    def json(self):
        if not self._json:
            self._json = loads(self.text)
        return self._json

    def __repr__(self):
        return f'<FastResponse [{self.status_code}]>'

    def __bool__(self):
        return self.status_code == 200

    def __str__(self):
        return f'<FastResponse [{self.status_code}]>'

class ConnectionsType(TypedDict):
    connection: HTTPConnection
    status: bool

class FastHTTPClient:

    def __init__(self, base_url: URL | str, *, timeout=120, debug: bool | Logger = False):
        if base_url.startswith('https://'):
            raise ValueError('FastHTTPClient 不支持https协议')
        if not base_url:
            raise ValueError('base_url 不能为空')
        base_url = base_url if isinstance(base_url, URL) else URL(base_url)
        self._base_url = urllib.parse.urlparse(base_url.url)
        self._timeout = timeout
        self.debug = debug
        self._connections: list[ConnectionsType] = []
        self._closed = False
        self.headers = {}
        self.debug = bool(debug)
        self._logger = debug if isinstance(debug, Logger) else logger

    @thread_lock
    def __get_connection(self) -> tuple[int, HTTPConnection]:
        if self._closed:
            raise ValueError("FastHTTPClient 已关闭")
        for index, connection in enumerate(self._connections):
            if not connection['status']:
                self._connections[index]['status'] = True
                return index, connection['connection']
        else:
            self._connections.append(
                {
                    "connection": HTTPConnection(self._base_url.netloc, timeout=self._timeout),
                    "status": True
                }
                )
            return len(self._connections) - 1, self._connections[-1]['connection']

    def set_token(self, token: str, key='Authorization'):
        if len(token.split(' ')) == 1:
            token = f"Bearer {token}"
        self.headers[key] = token

    @staticmethod
    def _encode_data_to_form_data(data):
        """将dict转换为multipart/form-data"""
        body = b''
        boundary = f'----{choose_boundary()}'
        content_type = f'multipart/form-data; boundary={boundary}'  # noqa
        for key, value in data.items():
            value = "" if value is None else str(value)
            body += f'--{boundary}\r\n'.encode('utf-8')
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')  # noqa
            body += f'{value}\r\n'.encode('utf-8')
        body += f'--{boundary}--'.encode('utf-8')
        return body, content_type

    def request(self, method, url: str, *, params=None, data=None, json=None, headers=None, **kwargs):
        if url.startswith('http://') or url.startswith('https://'):
            raise ValueError('URL不允许重新指定网络地址')
        if data and json:
            raise ValueError('data和json不能同时存在')
        if params:
            url = f'{url}?{urllib.parse.urlencode(params)}'
        if self.debug:
            method = method.upper()
            method_color = {
                'POST': Color.yellow, 'GET': Color.green, 'DELETE': Color.red, 'PUT': Color.magenta
            }.get(method, Color.cyan)
            self._logger.info(
                f'{method_color(method)} - {self._base_url.scheme}://{self._base_url.netloc}{url}', stacklevel=5
            )
        body = None
        if not headers:
            headers = {}
        if json:
            body = dumps(json, ensure_ascii=True)
            if self.debug:
                self._logger.info(f'Payload - {dumps(json, ensure_ascii=False)}', stacklevel=5)
            headers['Content-Type'] = 'application/json;charset=UTF-8'
        if data:
            body, content_type = self._encode_data_to_form_data(data)
            headers['Content-Type'] = content_type
            if self.debug:
                self._logger.info(f'Form data - {data}', stacklevel=5)
        index, conn = self.__get_connection()
        headers.update(self.headers)
        conn.request(method, url, body=body, headers=headers)
        response = FastResponse(conn.getresponse())
        self._connections[index][1] = False
        return response

    def get(self, url, *, params=None, headers=None):
        return self.request('GET', url, params=params, headers=headers)

    def post(self, url, *, data=None, json=None, headers=None):
        return self.request('POST', url, data=data, json=json, headers=headers)

    def put(self, url, *, data=None, headers=None):
        return self.request('PUT', url, data=data, headers=headers)

    def delete(self, url, *, data=None, headers=None):
        return self.request('DELETE', url, data=data, headers=headers)

    def close(self):
        for connection in self._connections:
            connection['connection'].close()
        self._connections.clear()
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    pass
