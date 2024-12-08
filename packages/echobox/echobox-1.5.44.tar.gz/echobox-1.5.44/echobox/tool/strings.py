import string
import random

import re
import six

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def random_str(count=10):
    return ''.join(random.choice(string.ascii_letters) for i in range(count))


def uncamelize_key(key):
    if not isinstance(key, six.string_types):
        return key
    s1 = first_cap_re.sub(r'\1_\2', key)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def uncamelize_value(value):
    if isinstance(value, six.string_types):
        return value
    if isinstance(value, dict):
        return {uncamelize_key(k): uncamelize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [uncamelize_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple((uncamelize_value(v) for v in value))
    return value


def camelize(key):
    return ''.join(s[0].upper() + s[1:] for s in key.split('_'))


def camelize_key(key):
    return '.'.join(camelize(x) for x in key.split('.'))


def camelize_value(value):
    if isinstance(value, six.string_types):
        return value
    if isinstance(value, dict):
        return {camelize_key(k): camelize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [camelize_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple((camelize_value(v) for v in value))
    return value
