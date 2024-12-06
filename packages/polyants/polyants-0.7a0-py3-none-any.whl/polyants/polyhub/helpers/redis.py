""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

import pickle

from time import sleep
from redis import Redis
from walrus import Database
from polyants.polyhub.constants import REDIS_PREFIX, DEFAULT_ID, REDIS_HOST, REDIS_PORT, REDIS_DB
from polyants.polyhub.enums import GenericState, ObjectType

RDB = Database(host=f'{REDIS_HOST}', port=REDIS_PORT, db=REDIS_DB)
RCG_CODE = f'{REDIS_PREFIX}group.skipper'
RS_CODE = 'stream-a'
AUTH_SETTINGS_KEY = f'{REDIS_PREFIX}settings:system:auth'


def get_redis():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def create_group():
    cg = RDB.consumer_group(RCG_CODE, [RS_CODE])
    cg.create()
    cg.set_id('$')
    return cg


def send_event(key, value, cg=None):
    cg = cg or create_group()
    cg.streams[RS_CODE].add({'data': pickle.dumps({'key': key, 'value': value})})


def get_auth_key(sid):
    """Параметры авторизации сессии."""
    return f'{REDIS_PREFIX}auth:{sid}'


def get_session_key(sid):
    return f'{REDIS_PREFIX}session:{sid}'


def get_sso_key(sid):
    """Ключ идентификатора сессии внешней авторизации."""
    return f'{REDIS_PREFIX}sso:{sid}'


def get_job_key(jobid):
    return f'{REDIS_PREFIX}job-{jobid}'


def get_job_status_key(jobid):
    return f'{REDIS_PREFIX}job-{jobid}-status'


def get_settings_key(user_id):
    return f'{REDIS_PREFIX}{user_id}:setting'


def get_object_settings_key(user_id, object_type, object_state=GenericState.UNKNOWN, object_id=DEFAULT_ID):
    object_state = object_state or GenericState.UNKNOWN
    return f'{get_settings_key(user_id)}:{object_type.value}:{object_state.value}:{object_id}'


def get_logout_key(sid):
    """Ключ идентификатора статуса завершенной сессии."""
    return f'{REDIS_PREFIX}logout:{sid}'


def get_permission_key(user_id, object_type, object_state=GenericState.UNKNOWN):
    object_state = object_state or GenericState.UNKNOWN
    return f'{REDIS_PREFIX}{user_id}:permission:{ObjectType(object_type).value}:{object_state.value}'


def get_user_keys(user_id):
    return f'{REDIS_PREFIX}{user_id}:*'


def get_stored_value(key, default=None, redis=None):
    redis = redis or get_redis()
    value = redis.get(key)
    default = value if default is None else default

    return value.decode() if value else default


def get_stored_object(key, redis=None):
    redis = redis or get_redis()
    encoded = redis.get(key)

    return pickle.loads(encoded) if encoded else None


def set_stored_value(key, value, seconds=None, keep_ttl=False, redis=None):
    redis = redis or get_redis()

    if seconds:
        redis.setex(key, int(seconds), value)
    else:
        redis.set(key, value, keepttl=keep_ttl)


def set_stored_object(key, value, seconds=None, keep_ttl=False, redis=None):
    set_stored_value(key, pickle.dumps(value), seconds=seconds, keep_ttl=keep_ttl, redis=redis)


def delete_stored_item(key, redis=None):
    redis = redis or get_redis()
    redis.delete(key)


def handle_event(cg, subscriptions):
    counter = 0
    while True:
        counter += 1
        event = cg.streams[RS_CODE].read()
        if event:
            for i in event:
                msg_id = i[0].decode()
                msg = pickle.loads(i[1][b'data'])

                if found := subscriptions.get(
                    msg['key'], subscriptions.get(msg['key'].replace(msg['key'][-len(DEFAULT_ID) :], DEFAULT_ID))
                ):

                    arguments = msg['value'].get('context', dict())
                    arguments.update(found.context or dict())
                    found.callback(found.object_id, found.user_id, arguments=arguments)

                cg.streams[RS_CODE].ack(msg_id)

        sleep(0.1)
