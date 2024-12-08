def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def merge(src, update):
    """
    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(a, b) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in update.items():
        if isinstance(value, dict):
            # get node or create one
            node = src.setdefault(key, {})
            merge(node, value)
        else:
            src[key] = value

    return src


def fetch(data, keys):
    """
    >>> data = [ {'k1': '1v1', 'k2': '1v2', 'k3': '1v3'}, {'k1': '2v1', 'k2': '2v2', 'k3': '2v3'}]
    >>> keys = ['k1', 'k3']
    >>> fetch(data, keys)
    [{'k1': '1v1', 'k3': '1v3'}, {'k1': '2v1', 'k3': '2v3'}]
    """
    ret = []
    for item in data:
        ret.append({key: item[key] for key in keys})
    return ret


def filter_by_key_value(data, key, value, count=1):
    """
    >>> data = [ {'k1': '1v1', 'k2': '1v2', 'k3': '1v3'}, {'k1': '2v1', 'k2': '2v2', 'k3': '2v3'}]
    >>> key = 'k1'
    >>> keys = '2v1'
    >>> filter_by_key_value(data, key, value)
    {'k1': '2v1', 'k3': '2v3'}
    """
    ret = list(filter(lambda item: (item[key] == value), data))
    if count == 1 and len(ret) > 0:
        return ret[0]
    return ret
