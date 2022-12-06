from pickle import dump, load
from __init__ import resource_dir


def __dump(data, filename):
    with open(resource_dir / filename, 'wb') as f:
        dump(data, f)
        f.close()


def __load(filename):
    with open(resource_dir / filename, 'rb') as f:
        data = load(f)
        f.close()
        return data


def insert(data, primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)
    if object_cache:
        for value in object_cache:
            if value[primaryKey] == valuePrimaryKey:
                remove(primaryKey, valuePrimaryKey, filename)
    object_cache.append(data)
    __dump(object_cache, filename)


def remove(primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)
    if object_cache:
        for data in object_cache:
            if data[primaryKey] == valuePrimaryKey:
                object_cache.remove(data)
    __dump(object_cache, filename)


def get(primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)
    if object_cache:
        for data in object_cache:
            if data[primaryKey] == valuePrimaryKey:
                return data
    return None


def get_all(filename):
    return __load(filename)
