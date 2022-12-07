from src.dao import get_all
from src.crypto import decrypt
from admin.key_store import admin_priv_key
from __init__ import resource_dir


def candidates():
    candidatesList = get_all(resource_dir / "candidates.pkl")
    result = []
    for data in candidatesList:
        candidate = [data["candidateId"], data["name"], data["party"]]
        result.append(candidate)
    return result


def count() -> dict:
    results = dict()
    registry = get_all(resource_dir / "urnVotes.pkl")
    for candidate in registry:
        encryptedVotes = candidate["votes"]
        candidateId = candidate["candidateId"]
        votes: int = decrypt(encryptedVotes, admin_priv_key)

        results[candidateId] = votes

    return results


if __name__ == '__main__':
    print(count())
