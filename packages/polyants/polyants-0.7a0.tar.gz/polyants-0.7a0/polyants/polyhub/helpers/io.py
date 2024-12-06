""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

from __future__ import annotations

import re
import json
import stat

from typing import Callable
from fnmatch import fnmatch
from pathlib import PosixPath
from dataclasses import dataclass
from pathvalidate import sanitize_filepath
from jsqlib.helpers.common import Tokenizer
from polyants.internal import log
from polyants.polyhub.exceptions import IOException
from polyants.polyhub.helpers.translit import to_latin
from polyants.polyhub.helpers.templater import JINJA


@dataclass
class ReportRecord:
    path: PosixPath = PosixPath('')
    depth: int = 0
    folder: bool | None = False
    symlink: bool = False
    matched: bool = True
    missing: bool = False
    hidden: bool = False
    root: bool = False
    error: bool = False
    slug: str = ''
    message: str = ''


def get_clean_path(path, as_string=True, strict=True):
    error_msg = f'Путь {path} некорректен. Содержит `.`'

    if './' in str(path):
        raise IOException(error_msg)

    clean = sanitize_filepath(path)

    if strict and clean != path:
        raise IOException(f'Путь {path} невалиден. ')

    if './' in str(clean):
        raise IOException(error_msg)

    return clean if as_string else PosixPath(clean)


def get_relative_path(path, as_string=True):
    return get_clean_path(path.strip('.').strip('/'), as_string=as_string)


def get_file_content(path: str | PosixPath, as_json=False, as_bytes=False):
    content = b'' if as_bytes else ''
    path = PosixPath(path)

    if path.is_file():
        try:
            content = path.read_bytes() if as_bytes else path.read_text()
        except Exception as e:
            raise IOException(f'Не удалось получить содержимое {path}, ошибка: {e}')

    return json.loads(content.decode() if as_bytes else content) if content and as_json else content  # pyre-ignore[16]


def get_safe_name(name):
    """Перекодирует наименование в более удобное при обработке в файловой системе.
    TODO: желательно добавить возможность отключения по настройке или даже несколько уровней.
    """
    name = to_latin(get_clean_path(name))
    safe_re = re.compile(r'[^a-zа-я0-9-]', re.IGNORECASE)  # @UndefinedVariable
    return safe_re.sub('_', name)


def get_safe_path(path):
    result = None

    if path:
        path = get_relative_path(path)
        result = '/'.join([get_safe_name(i) for i in path.split('/')])

    return result


def get_joined_path(parent, child):
    parent = f'{get_relative_path(parent)}/' if parent else ''
    child = get_relative_path(child) if child else ''

    return f'{parent}{child}'


def render_text(text, binds=None):
    if binds is None:
        binds = dict()

    return JINJA.from_string(text).render(binds)


def render_template(path, binds=None, default=None, as_json=True):
    if not path.is_file():
        if default is not None:
            return default

        raise IOException(f'Не найден файл шаблона {path}')

    template = path.read_text()

    try:
        rendered = render_text(template, binds=binds)
    except Exception as e:
        log.error('Ошибка рендеринга: %s\nФайл: %s\nПеременные: %s\n Шаблон: %s', e, path, template, binds)
        raise e

    log.debug('Результат рендеринга %s: %s', path, rendered)

    return json.loads(rendered) if as_json else rendered


def set_file_content(path: str | PosixPath, content, as_json=False, as_bytes=False, create_dirs=False):
    path = PosixPath(path)
    if create_dirs:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise IOException(f'Не удалось создать директорию {path}, ошибка: {e}')

    content = json.dumps(content) if as_json else content
    try:
        content = path.write_bytes(content) if as_bytes else path.write_text(content)
    except Exception as e:
        raise IOException(f'Не удалось записать данные в {path}, ошибка: {e}')


def render_jsql(raw, arguments=None, as_json=True):
    arguments = arguments or dict()
    raw = json.dumps(raw) if isinstance(raw, (dict, list)) else raw
    rendered = Tokenizer(constants=arguments).stringify(raw)

    return json.loads(rendered) if as_json else rendered


def render_mock(raw, arguments=None, as_json=True):
    raw = json.dumps(raw) if isinstance(raw, (dict, list)) else raw
    arguments = arguments or dict()

    for k, v in arguments.items():
        raw = raw.replace(f'"{k}"', v)

    return json.loads(raw) if as_json else raw


def guess_dir_entry_type(entry: PosixPath, follow_symlinks=True) -> str:
    try:
        stat_info = entry.stat(follow_symlinks=follow_symlinks)
    except Exception:
        result = 'unknown'
    else:
        match stat.S_IFMT(stat_info.st_mode):
            case stat.S_IFLNK:
                result = 'symlink'
            case stat.S_IFSOCK:
                result = 'socket'
            case stat.S_IFIFO:
                result = 'pipe'
            case stat.S_IFCHR:
                result = 'chardev'
            case stat.S_IFBLK:
                result = 'blockdev'
            case stat.S_IFREG:
                result = 'file'
            case stat.S_IFDIR:
                result = 'folder'
            case _:
                result = 'unknown'

    return result


def is_broken_path(path: PosixPath) -> bool:
    try:
        path.resolve(strict=True)
        return False
    except FileNotFoundError:
        return True


def is_hidden_path(path: PosixPath) -> bool:
    if path.name.startswith('.'):
        return True
    return False


def rec_record(
    report: list[ReportRecord] | None,
    record: ReportRecord | None,
    relative_root: PosixPath | None = None,
    write_report: bool = True,
) -> None:
    if write_report and record and report is not None:
        if relative_root and record.path:
            record.path = record.path.relative_to(relative_root)
        report.append(record)


def get_path_depth(path: PosixPath, relative_root: PosixPath | None) -> int:
    """Вычисляет глубину пути.
    Уровень содержимого relative_root - 0.
    """
    if relative_root:
        path = path.relative_to(relative_root)
        print(f'{path=}, {len(path.parts)=}')

    return len(path.parts) - 1


def process_folder(
    root: PosixPath,
    folder_handler: Callable[[PosixPath, int], ReportRecord | None] | None = None,
    file_handler: Callable[[PosixPath, int], ReportRecord | None] | None = None,
    folder_patterns: list[str] | None = None,
    file_patterns: list[str] | None = None,
    skip_symlinks: bool = False,
    skip_missing: bool = True,
    skip_hidden: bool = True,
    skip_root: bool = True,
    write_report: bool = True,
    max_depth: int = 0,
    relative_root: PosixPath | None = None,
) -> list[ReportRecord] | None:
    stack = list()
    report = list() if write_report else None
    current_depth = get_path_depth(root, relative_root=relative_root)

    if skip_symlinks and root.is_symlink():
        rec_record(
            report,
            ReportRecord(root, depth=current_depth, folder=root.is_dir(), symlink=True, root=True),
            relative_root=relative_root,
            write_report=write_report,
        )
        return report

    if skip_missing and is_broken_path(root):
        rec_record(
            report,
            ReportRecord(root, depth=current_depth, folder=root.is_dir(), missing=True, root=True),
            relative_root=relative_root,
            write_report=write_report,
        )
        return report

    if skip_hidden and is_hidden_path(root):
        rec_record(
            report,
            ReportRecord(root, depth=current_depth, folder=root.is_dir(), hidden=True, root=True),
            relative_root=relative_root,
            write_report=write_report,
        )
        return report

    if root.is_dir():
        stack.append(root)

        while stack:
            current = stack.pop()

            if folder_handler:
                if current == root:
                    if skip_root:
                        rec_record(
                            report,
                            ReportRecord(root, depth=current_depth, folder=True, root=True),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                    else:
                        rec_record(
                            report,
                            folder_handler(root, current_depth),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                else:
                    current_depth = get_path_depth(current, relative_root=relative_root)
                    if max_depth == 0 or current_depth <= max_depth:
                        rec_record(
                            report,
                            folder_handler(current, current_depth),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                    else:
                        rec_record(
                            report,
                            ReportRecord(current, depth=current_depth, folder=True),
                            relative_root=relative_root,
                            write_report=write_report,
                        )

            for entry in current.iterdir():
                current_depth = get_path_depth(entry, relative_root=relative_root)

                if max_depth == 0 or current_depth <= max_depth:
                    if skip_symlinks and entry.is_symlink():
                        rec_record(
                            report,
                            ReportRecord(entry, depth=current_depth, folder=entry.is_dir(), symlink=True),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                        continue

                    if skip_missing and is_broken_path(entry):
                        rec_record(
                            report,
                            ReportRecord(entry, depth=current_depth, folder=entry.is_dir(), missing=True),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                        continue

                    if skip_hidden and is_hidden_path(entry):
                        rec_record(
                            report,
                            ReportRecord(entry, depth=current_depth, folder=entry.is_dir(), hidden=True),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                        continue

                    if entry.is_dir():
                        if folder_patterns is None:
                            stack.append(entry)
                        else:
                            for pattern in folder_patterns:
                                if fnmatch(entry.name, pattern):
                                    stack.append(entry)
                                    break
                            else:
                                rec_record(
                                    report,
                                    ReportRecord(entry, depth=current_depth, folder=True, matched=False),
                                    relative_root=relative_root,
                                    write_report=write_report,
                                )
                    elif entry.is_file():
                        if file_handler is not None:
                            if file_patterns is None:
                                rec_record(
                                    report,
                                    file_handler(entry, current_depth),
                                    relative_root=relative_root,
                                    write_report=write_report,
                                )
                            else:
                                for pattern in file_patterns:
                                    if fnmatch(entry.name, pattern):
                                        rec_record(
                                            report,
                                            file_handler(entry, current_depth),
                                            relative_root=relative_root,
                                            write_report=write_report,
                                        )
                                        break
                                else:
                                    rec_record(
                                        report,
                                        ReportRecord(entry, depth=current_depth, matched=False),
                                        relative_root=relative_root,
                                        write_report=write_report,
                                    )
                    elif write_report:
                        rec_record(
                            report,
                            ReportRecord(
                                entry,
                                depth=current_depth,
                                error=True,
                                message=f'Unsupported entry type: {guess_dir_entry_type(entry)}',
                            ),
                            relative_root=relative_root,
                            write_report=write_report,
                        )
                else:
                    rec_record(
                        report,
                        ReportRecord(current, depth=current_depth),
                        relative_root=relative_root,
                        write_report=write_report,
                    )
    else:
        rec_record(
            report,
            ReportRecord(root, depth=current_depth, root=True),
            relative_root=relative_root,
            write_report=write_report,
        )

    return report


def is_only_dirs(path: PosixPath | str) -> bool:
    """Возвращает True, только если все обекты в директории тоже директории."""
    for entry in PosixPath(path).iterdir():
        if entry.is_file() or (entry.is_dir() and not is_only_dirs(entry)):
            return False

    return True
