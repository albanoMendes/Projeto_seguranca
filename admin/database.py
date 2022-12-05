from src.database import cursor
from src.crypto import decrypt
from admin.keystore import admin_priv_key


def candidates():
    query = 'SELECT * FROM Candidate;'
    cursor.execute(query)

    result = cursor.fetchall()
    return result


def count() -> dict:
    results = dict()

    query = 'SELECT * FROM UrnVote;'
    cursor.execute(query)

    registry: tuple = cursor.fetchall()
    for candidate in registry:
        candidate_id, votes = candidate
        votes: str = votes
        votes: bytes = eval(votes)
        votes: int = decrypt(votes, admin_priv_key)

        results[candidate_id] = votes

    return results


if __name__ == '__main__':
    print(count())
