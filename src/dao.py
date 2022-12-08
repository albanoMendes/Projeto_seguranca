import pickle


def dump(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        return data


def dump_vote(encrypted_vote, filename):
    object_cache = load(filename)
    object_cache.append(encrypted_vote)
    dump(object_cache, filename)
