""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

from __future__ import annotations

import json

from typing import Union
from io import BytesIO
from base64 import b64encode, urlsafe_b64encode
from hashlib import md5
from polyants.polyhub.constants import DICT_HASH, LIST_HASH
from polyants.polyhub.exceptions import AdapterException


def to_json(value, sort_keys=True, ensure_ascii=False) -> str:
    return json.dumps(value, ensure_ascii=ensure_ascii, separators=(',', ':'), sort_keys=sort_keys, default=str)


def to_md5(value, encode=True) -> Union[str | bytes]:
    encoded = bytes(value, encoding='utf-8') if encode and value else value
    return md5(encoded).hexdigest() if encoded else encoded


def to_hash(value, as_guid=False, sort_keys=True, ensure_ascii=False) -> Union[bytes, str]:
    hash_ = None
    encode = True
    value_type = type(value)

    if value_type in (int, float):
        value = str(value)
    elif value_type is list:
        hash_ = to_md5(to_json(value, sort_keys=sort_keys, ensure_ascii=ensure_ascii)) if value else LIST_HASH
    elif value_type is dict:
        hash_ = to_md5(to_json(value, sort_keys=sort_keys, ensure_ascii=ensure_ascii)) if value else DICT_HASH
    elif value_type is bytes:
        encode = False
    elif value_type == BytesIO:
        encode = False
        value = value.getvalue()

    hash_ = hash_ or to_md5(value, encode=encode)

    return f"{hash_[:8]}-{hash_[8:12]}-{hash_[12:16]}-{hash_[16:20]}-{hash_[20:]}" if as_guid else hash_


def file_to_md5(path):
    hash_md5 = md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def json_to_crontab(timetable):
    minute = str(timetable.get('minute', '*'))
    hour = str(timetable.get('hour', '*'))
    day_of_week = str(timetable.get('day_of_week', '*'))
    day_of_month = str(timetable.get('day_of_month', '*'))
    month_of_year = str(timetable.get('month_of_year', '*'))

    return ' '.join((minute, hour, day_of_month, month_of_year, day_of_week))


def decapitalize(s):
    return s[0].lower() + s[1:]


def snake_to_upper_camel(s):
    return ''.join([word.capitalize() for word in s.split('_')])


def snake_to_camel(s):
    return decapitalize(snake_to_upper_camel(s))


def dot_to_dict(path, value):
    """Конвертирует сокращенную запись словаря настроек в словарь.
    TODO: использовать polyants get_by_pointer?
    """
    result = {'value': value.get('value')}
    path = path.replace('.', '/')
    paths = path.split('/')

    for idx, p in enumerate(paths[::-1]):
        if idx == 0:
            result = {p: result}
        else:
            result = {p: {'value': result}}

    return result


def to_bytes(value: str | bytes) -> bytes:
    if isinstance(value, str):
        value = value.encode()

    return value


def to_base64(value: str | bytes, as_string=True) -> bytes | str:
    encoded = b64encode(to_bytes(value))

    return encoded.decode() if as_string else encoded


def to_urlsafe_base64(value: str | bytes, as_string=True) -> bytes | str:
    encoded = urlsafe_b64encode(to_bytes(value))

    return encoded.decode() if as_string else encoded


def to_plain_json(data: dict | list, out: dict | list | None = None) -> dict | list:
    """Убирает из переданного json служебную мету и убирает обертки `content` у атрибутов.
    Распакованный json используется исключительно для валидации, в базе не хранится.
    TODO: перейти на итераторы и ijson
    """
    if out is None:
        # служебный уровень, данные ниже должны собраться в новый объект
        if (not isinstance(data, dict)) or (float(data.get('version', 2.0)) < 2.0) or 'content' not in data:
            # версия без меты
            return data

        out = to_plain_json(data['content'], out=dict())
    else:
        # список из вышестоящего 'content'
        for i in data:
            if 'content' in i:
                # шорткат ключа либо индекса будущего элемента
                attribute = i['attribute']

                if i['type'] == 'object':
                    content = i['content']
                    if isinstance(out, dict):
                        out[attribute] = to_plain_json(content, out=dict())
                    else:
                        out.append(to_plain_json(content, out=dict()))
                else:
                    content = sorted(i['content'], key=lambda i: i['attribute'])
                    if isinstance(out, dict):
                        out[attribute] = to_plain_json(content, out=list())
                    else:
                        out.append(to_plain_json(content, out=list()))
            elif 'value' in i:
                # примитив или объект/список без меты, добавляем и возвращаем
                if isinstance(out, dict):
                    # присваиваем значение ключу
                    out[i['attribute']] = i['value']
                else:
                    # добавляем элемент в конец, т.к. до вызова 'content' отсортирован
                    out.append(i['value'])
            else:
                raise AdapterException('Не найдены ключи данных')
    return out
