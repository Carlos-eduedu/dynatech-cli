from enum import Enum


class ExporterType(str, Enum):
    none = "none"
    json = "json"
    txt = "txt"
