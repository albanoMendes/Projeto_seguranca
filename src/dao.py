import pickle
from __init__ import resource_dir


def dump(data, filename):
    with open(resource_dir / filename, 'wb') as f:
        pickle.dump(data, f)


def __load(filename):
    with open(resource_dir / filename, 'rb') as f:
        data = pickle.load(f)
        return data


def insert(data, primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)

    if object_cache:
        for value in object_cache:
            if value[primaryKey] == valuePrimaryKey:
                return False

    object_cache.append(data)
    dump(object_cache, filename)
    return True


def remove(primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)
    if object_cache:
        for data in object_cache:
            if data[primaryKey] == valuePrimaryKey:
                object_cache.remove(data)
    dump(object_cache, filename)


def get(primaryKey, valuePrimaryKey, filename):
    object_cache = __load(filename)
    if object_cache:
        for data in object_cache:
            if data[primaryKey] == valuePrimaryKey:
                return data
    return None


def get_all(filename):
    return __load(filename)
