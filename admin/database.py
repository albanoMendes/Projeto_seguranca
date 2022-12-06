from src.dao import get_all
# from src.database import cursor
from src.crypto import decrypt
from admin.keystore import admin_priv_key
from __init__ import resource_dir


def candidates():
    # query = 'SELECT * FROM Candidate;'
    # cursor.execute(query)
    #
    # result = cursor.fetchall()
    candidatesList = get_all(resource_dir / "candidates.pkl")
    result = []
    for data in candidatesList:
        candidate = [data["candidateId"], data["name"], data["party"]]
        result.append(candidate)
    return result


def count() -> dict:
    results = dict()

    # query = 'SELECT * FROM UrnVote;'
    # cursor.execute(query)
    #
    # registry: tuple = cursor.fetchall()
    registry = get_all(resource_dir / "urnVotes.pkl")
    # for candidate in registry:
    #     candidate_id, votes = candidate
    #     votes: str = votes
    #     votes: bytes = eval(votes)
    #     votes: int = decrypt(votes, admin_priv_key)
    for candidate in registry:
        encryptedVotes = candidate["votes"]
        candidateId = candidate["candidateId"]
        votes: int = decrypt(encryptedVotes, admin_priv_key)

        results[candidateId] = votes

    return results


if __name__ == '__main__':
    print(count())
