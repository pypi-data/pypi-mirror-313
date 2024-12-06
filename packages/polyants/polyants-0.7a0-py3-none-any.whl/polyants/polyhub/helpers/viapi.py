""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

import re
import requests

from datetime import timedelta
from requests.compat import urljoin
from polyants.polyhub.helpers.common import get_now
from polyants.polyhub.exceptions import ViApiException

re_units = {
    'viqube': re.compile(r'\/?viqube\/.+', flags=re.RegexFlag.IGNORECASE),
    'dc': re.compile(r'\/?datacollection\/.+', flags=re.RegexFlag.IGNORECASE),
}


def get_unit(url):
    for k, v in re_units.items():
        if v.match(url):
            unit = k
            break
    else:
        raise ViApiException(f'Неизвестный тип запроса Visiology: {url}')

    return unit


class Hook:
    """Класс взаимодействия с API сервиса Visiology."""

    def __init__(self, provider, unit='viqube', **kwargs):
        """Инициализация параметров подключения"""
        self.provider = provider
        options = provider.options or dict()
        self.batch = options.get('batch', 10000)
        self.pool = options.get('pool', 10)
        self._unit = unit
        self._context = {
            'api': None,
            'user': provider.login,
            'pass': provider.password,
            'url': provider.host,
            'options': options,
        }

        self.conn = self._get_conn()
        self.connected = False

    @property
    def token(self):
        if self._is_token_expired():
            self.conn = self._get_conn()

        return self.conn['token']

    @property
    def auth_string(self):
        if self._is_token_expired():
            self.conn = self._get_conn()

        return f"{self.conn['token_type']} {self.conn['token']}"

    def _parse_response(self, response):
        content_type = response.headers.get('Content-Type')
        if content_type and response.text and 'application/json' in content_type:
            result = response.json()
        else:
            result = response.text
        return result

    def _get_conn(self):
        # убрать либо исправить scopes, как ни на что не влияющий при получении токена ключ
        ctx = self._context
        conn = dict()
        scope_name = 'scopes'
        scope = ctx['options'].get('scopes')
        authorization = ctx['options'].get('authorization')

        if self._unit == 'viqube':
            scope = ctx['options'].get('scope', 'viqube_api viqubeadmin_api')
            scope_name = 'scope'
            authorization = authorization or 'Basic dmlxdWJlYWRtaW5fcm9fY2xpZW50OjcmZEo1UldwVVMkLUVVQE1reHU='
        elif self._unit == 'dc':
            scope = scope or 'viewer_api core_logic_facade'
        elif self._unit == 'dash':
            scope = scope or 'viqube_api viewer_api'
        elif 'scope' in ctx['options'] and 'scopes' not in ctx['options']:
            scope = ctx['options']['scope']
            scope_name = 'scope'
        else:
            unit_str = self._unit or 'без scope'
            raise ViApiException(f'API подсистемы Visiology <{unit_str}> не поддерживается')

        authorization = authorization or 'Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ=='
        grant_type = ctx['options'].get('grant_type', 'password')
        response_type = ctx['options'].get('response_type', 'id_token token')
        conn['entry_point'] = ctx['url']
        conn['verify'] = ctx['options'].get('ssl_verify', True)

        if not ctx['api']:
            if self._unit == 'viqube':
                # запрашиваем версию API у целевого сервиса
                url = urljoin(conn['entry_point'], 'viqube/version')

                try:
                    r = requests.get(url=url, verify=conn['verify'])
                except Exception as e:
                    raise ViApiException(f'Ошибка получения версии API:\n{e}')

                if r.status_code == requests.codes.ok:  # @UndefinedVariable
                    ctx['api'] = r.json()['apiStable']
                else:
                    answer = self._parse_response(r)
                    msg = f'Http ошибка при полученнии версии API: код = {r.status_code}, ответ:\n{answer}'
                    raise ViApiException(msg)
            elif self._unit == 'dc':
                ctx['api'] = '1.0'

        conn['api_version'] = ctx['api']

        params = {
            'grant_type': grant_type,
            scope_name: scope,
            'response_type': response_type,
            'username': ctx['user'],
            'password': ctx['pass'],
        }

        url = urljoin(conn['entry_point'], 'idsrv/connect/token')

        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': authorization}

        try:
            r = requests.post(url=url, headers=headers, data=params, verify=conn['verify'])
        except Exception as e:
            raise ViApiException(f'Ошибка получения токена:\n{e}')

        if r.status_code == requests.codes.ok:  # @UndefinedVariable
            token = r.json()
        else:
            answer = self._parse_response(r)
            msg = f'Http ошибка при полученнии токена: {r.status_code}, ответ:\n{answer}'
            raise ViApiException(msg)

        conn['token'] = token['access_token']
        conn['token_type'] = token['token_type']

        conn['token_expires'] = get_now() + timedelta(seconds=token['expires_in'])

        return conn

    def _request(self, method, url, headers=None, data=None):
        try:
            self.connected = True
            r = requests.request(method, url, headers=headers, json=data)
            self.connected = False
        except Exception as e:
            headers['Authorization'] = '*******'
            raise ViApiException(f'{method.upper()} [{url}], хидеры:\n{headers}\nошибка:\n{e}')

        return r

    def _is_token_expired(self):
        return get_now() >= self.conn['token_expires']

    def _update_headers(self, extra_headers=None):
        headers = {'Authorization': self.auth_string}

        if self.conn['api_version']:
            headers['X-API-VERSION'] = self.conn['api_version']

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def call(self, resource, method='post', extra_headers=None, data=None):
        """Универсальный вызов API.
        Args:
            :resource - адрес ресурса относительно API entry point
            :method - тип сообщения, обычно get или post
            :extra_headers - http заголовки, дополняющие, либо переопределяющие стандартные
            :data - полезная нагрузка запроса, как правило - словарь
        Returns:
            Ответ сервера, как правило - в виде словаря
        """
        headers = self._update_headers()

        url = urljoin(self.conn['entry_point'], resource)

        if self._is_token_expired():
            # обновляем токен по времени
            self.conn = self._get_conn()
            headers = self._update_headers()

        r = self._request(method, url, headers=headers, data=data)
        answer = self._parse_response(r)

        if r.status_code == requests.codes.forbidden and 'token expired' in answer:  # @UndefinedVariable
            # пытаемся обновить токен по ошибке
            self.conn = self._get_conn()
            headers = self._update_headers()

            r = self._request(method, url, headers=headers, data=data)
            answer = self._parse_response(r)

        if r.status_code != requests.codes.ok:  # @UndefinedVariable
            data = f'\nтело:\n{data}' if data is not None else ''
            msg = f'{method.upper()} [{url}], код ошибки: {r.status_code}, ответ:\n{answer}{data}'
            raise ViApiException(msg)

        return answer

    def disconnect(self):
        self.connected = False
