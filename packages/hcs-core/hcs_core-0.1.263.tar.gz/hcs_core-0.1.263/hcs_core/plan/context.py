_data = {}


def reset():
    _data.clear()


def get(k):
    return _data.get(k)


def set(k, v):
    _data[k] = v
