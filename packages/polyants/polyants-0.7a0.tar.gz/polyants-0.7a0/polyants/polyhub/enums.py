""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 13, 2024

@author: pymancer@gmail.com (polyanalitika.ru)
"""

from enum import IntFlag, Enum, auto


class AutoValueEnum(Enum):
    def _generate_next_value_(self, start, count, last_values):
        """Возвращает значение в camelCase,
        преобразуя `_x` в прописные буквы,
        остальные - в строчные.
        """
        value = self
        converted = list()
        upper = False

        for c in value:
            if c == '_':
                upper = True
                continue

            if upper:
                converted.append(c.upper())
                upper = False
            else:
                converted.append(c.lower())

        return ''.join(converted)


class ReportInstanceFormat(AutoValueEnum):
    DOCX = auto()
    HTML = auto()
    PDF = auto()
    PPTX = auto()
    RTF = auto()
    XLS = auto()
    XLSX = auto()
    TXT = auto()


class GenericState(IntFlag):
    """Перечисление состояний типового объекта.
    Индивидуальные перечисления состояний должны включать его элементы.
    """

    UNKNOWN = 0
    DELETED = auto()
    ACTIVE = auto()
    INVALID = auto()


class AuthType(AutoValueEnum):
    LOCAL = auto()
    LDAP = auto()
    OAUTH = auto()
    VISIOLOGY = auto()


class ProviderType(AutoValueEnum):
    LOCAL = auto()  # fs
    JSON = auto()  # db (INTERNAL)
    POSTGRESQL = auto()
    MSSQL = auto()
    VIQUBE = auto()
    HTTP = auto()
    HTTPS = auto()
    DWH = auto()  # Polyflow
    EMAIL = auto()
    TELEGRAM = auto()
    MONGO = auto()
    PLAINFS = auto()


class AccessrightType(IntFlag):
    UNKNOWN = 0
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    MANAGE = auto()
    CREATE = auto()
    ACTIVATE = auto()


class ReportType(AutoValueEnum):
    DOCX = auto()
    JRXML = auto()
    XLSX = auto()
    HTML = auto()


class ReportInstancePhase(AutoValueEnum):
    REQUESTED = auto()
    QUEUED = auto()
    GENERATING = auto()
    GENERATED = auto()
    POPULATING = auto()
    POPULATED = auto()
    DISCARDED = auto()
    FAILED = auto()


class PermissionScope(AutoValueEnum):
    GROUP = auto()
    OBJECT = auto()


class CloudObjectType(AutoValueEnum):
    NODE = auto()
    FOLDER = auto()
    FILE = auto()


class EntryOperation(AutoValueEnum):
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()


class TaskType(AutoValueEnum):
    QUEUE = auto()
    ASYNC = auto()


class ScheduleType(AutoValueEnum):
    INTERVAL = auto()
    TIMEDELTA = auto()
    CRONTAB = auto()
    SOLAR = auto()


class DwhFamily(AutoValueEnum):
    MODELS = auto()
    RULES = auto()


class BucketCapability(AutoValueEnum):
    LIST_FILES = auto()
    READ_FILES = auto()
    WRITE_FILES = auto()
    DELETE_FILES = auto()


class DatagridCapability(AutoValueEnum):
    READ_ENTRIES = auto()
    ADD_ENTRIES = auto()
    EDIT_ENTRIES = auto()
    DELETE_ENTRIES = auto()


class ReportCapability(AutoValueEnum):
    LIST_INSTANCES = auto()
    READ_INSTANCES = auto()
    WRITE_INSTANCES = auto()
    DELETE_INSTANCES = auto()


class AlertCapability(AutoValueEnum):
    EXECUTE_TRIGGER = auto()


class OrchestratorCore(AutoValueEnum):
    DAGSTER = auto()
    AIRFLOW = auto()


class EventType(IntFlag):
    UNKNOWN = auto()
    MANAGE = auto()
    CREATE = auto()
    EXECUTE = auto()
    PERMIT = auto()
    FORBID = auto()
    TWEAK = auto()
    UPDATE = auto()
    ACTIVATE = auto()
    DEACTIVATE = auto()
    DELETE = auto()
    RESTORE = auto()
    PURGE = auto()
    EDIT = auto()
    LOGIN = auto()
    LOGOUT = auto()
    STREAM = auto()


class ObjectType(IntFlag):
    """Тип объекта (Класс).
    Все управляемые, т.е. поддерживающие настройки и разрешения, типы объектов должны быть в этом перечислении.
    Битовые комбинации позволяют привязку настроек сразу к нескольким типам объектов (без object_id).
    """

    UNKNOWN = 0
    SYSTEM = auto()
    USER = auto()
    GROUP = auto()
    ACCESSRIGHT = auto()
    SETTING = auto()
    PROVIDER = auto()
    REPORT = auto()
    BUCKET = auto()
    DATAGRID = auto()
    JSONSCHEMA = auto()
    DWHMODEL = auto()
    TASK = auto()
    SCHEDULE = auto()
    DWHRULE = auto()
    WINDOW = auto()
    ALERT = auto()
    FILLER = auto()
    ORCHESTRATOR = auto()
    DUMMY = auto()
    SCRIPT = auto()
    REPOSITORY = auto()


class ScriptType(AutoValueEnum):
    PYTHON = auto()
    SQL = auto()
    SH = auto()
