""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

from functools import cache
from collections import defaultdict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from polyants.polyhub.constants import APP_CODE, BACK_CODE, REPORT_CODE, ALERT_CODE, SKIPPER_CODE
from polyants.polyhub.helpers.http import get_protocol


class DefaultDict(defaultdict):
    def __missing__(self, key):
        return self.default_factory(key)


def client_factory(code):
    return Client(
        transport=RequestsHTTPTransport(
            url=f'http://{APP_CODE}-{code}:3000/graphql',
        )
    )


@cache
def get_clients():
    clients = DefaultDict(client_factory)
    clients.update(
        {
            BACK_CODE: Client(
                transport=RequestsHTTPTransport(
                    url=f'{get_protocol()}://{APP_CODE}-{BACK_CODE}:3000/api/graphql',
                )
            ),
            REPORT_CODE: Client(
                transport=RequestsHTTPTransport(
                    url=f'http://{APP_CODE}-{REPORT_CODE}:3000/graphql',
                )
            ),
            ALERT_CODE: Client(
                transport=RequestsHTTPTransport(
                    url=f'http://{APP_CODE}-{ALERT_CODE}:3000/graphql',
                )
            ),
            SKIPPER_CODE: Client(
                transport=RequestsHTTPTransport(
                    url=f'http://{APP_CODE}-{SKIPPER_CODE}:3000/graphql',
                )
            ),
        }
    )

    return clients


def execute(query, params=None, client_code=BACK_CODE):
    return get_clients()[client_code].execute(gql(query), variable_values=params)
