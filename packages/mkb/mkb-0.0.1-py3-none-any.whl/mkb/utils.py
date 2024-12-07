import json
from string import Formatter
from datetime import datetime


def extract_required_keywords(template_str):
    """
    Extract named keywords from a string template.
    :param template_str: string template.
    :return: list of named keywords.
    """
    return [fn for _, fn, _, _ in Formatter().parse(template_str) if fn is not None]


def try_parse_json(js):
    """
    Parse the given string as json. If it cannot be parsed, return the original string.
    :param js: json string.
    :return: parsed dict object, or the original string if it cannot be parsed.
    """
    try:
        dict_ret = json.loads(js)
        return dict_ret, True
    except ValueError as e:
        return js, False


def get_datetime_str():
    """
    return string representation of the current format like 2024-11-30-13-15-59
    :return:
    """
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def append_datetime(name: str):
    return name + "_" + get_datetime_str()
