from enum import Enum


class Context(str, Enum):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    DANGER = 'danger'
