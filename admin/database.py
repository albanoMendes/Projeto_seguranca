from src.crypto import decrypt
from src.dao import load
from admin.key_store import admin_priv_key
from __init__ import candidates_file


def candidates():
    to_vote = load(candidates_file)
    result = list()

    for data in to_vote:
        result.append((data['candidate_id'], data['name'], data['party']))

    return result


def count() -> dict:
    results = dict()
    registry = load(candidates_file)

    for candidate in registry:
        encrypted_votes = candidate['votes']
        candidate_id = candidate['candidate_id']
        votes: int = decrypt(encrypted_votes, admin_priv_key)

        results[candidate_id] = votes

    return results


if __name__ == '__main__':
    print(count())
