from enum import Enum
import dateutil
from datetime import timedelta
import re

from azureml.studio.core.utils.yamlutils import register_yaml_representer

_re_timedelta = re.compile(
    r'^\s*(?P<x>-?)((?P<d>\d+)\.)?(?P<h>\d{1,2}):(?P<m>\d{1,2})(:(?P<s>\d{1,2})(\.(?P<f>\d{1,6}))?)?\s*$')


class AutoEnum(Enum):
    def __new__(cls, *args):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        # Enable to dump to yaml
        register_yaml_representer(cls, cls.to_yaml)
        return obj

    @staticmethod
    def to_yaml(representer, obj):
        from azureml.studio.modulehost.attributes import ItemInfo
        name = ItemInfo.get_enum_friendly_name(obj)
        return representer.represent_str(name)


def get_enum_values(enum_type: type):
    if not issubclass(enum_type, Enum):
        raise Exception("{0} is not subclass of Enum.".format(enum_type))
    return [e for e in enum_type]


def is_null_or_empty(s: str):
    """
    >>> is_null_or_empty("")
    True
    >>> is_null_or_empty(None)
    True
    >>> is_null_or_empty(" ")
    False
    """
    return s is None or s == ""


def is_null_or_whitespace(s: str):
    """
    >>> is_null_or_whitespace("")
    True
    >>> is_null_or_whitespace(None)
    True
    >>> is_null_or_whitespace(" ")
    True
    """
    return is_null_or_empty(s) or s.isspace()


def parse_datetime(s: str):
    return dateutil.parser.parse(s, dayfirst=False, yearfirst=True)


def parse_timedelta(s: str):
    """
    Convert a C# like string representation of TimeSpan to python timedelta.

    Valid format:
        [-][d.]H:m[:s[.f[f[f[f[f[f]]]]]]]

    Example:
        "1:2", "1:02", "01:02" -> 1h 2m
        "01:02:03" -> 1h 2m 3s
        "-01:02:03" -> -1h 2m 3s
        "4.01:02:03" -> 4d 1h 2m 3s
        "4.01:02:03.46" -> 4d 1h 2m 3s 460ms
        "4.01:02:03.468357" -> 4d 1h 2m 3s 468ms 357μs

    :param s: string to convert.
    :return: a timedelta value.
    """
    mat = _re_timedelta.match(s)
    if mat is None:
        raise ValueError(f"Failed parse {s} to timedelta, invalid format.")
    dd, hh, mm, ss, ff = (int(mat.group(grp)) if mat.group(grp) else 0 for grp in 'dhmsf')
    if not (0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59):
        raise ValueError(f"Failed parse {s} to timedelta, at least one of the components is outside its valid range.")
    if mat.group('x') == '-':
        dd = -dd
    seconds = hh * 3600 + mm * 60 + ss
    microseconds = 10**(6-len(str(ff)))*ff
    return timedelta(days=dd, seconds=seconds, microseconds=microseconds)
