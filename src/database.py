from phe import PaillierPublicKey, PaillierPrivateKey
from src.crypto import encrypt, decrypt
from src.key_store import private_key_from
from admin.key_store import admin_pub_key
from __init__ import candidates_file, user_votes_file
from src.dao import dump_vote, dump, load
from os.path import isfile


def urn():
    if isfile(candidates_file) or isfile(user_votes_file):
        return

    candidates = [{'candidate_id': 0,
                   'name': 'Zé da Padaria',
                   'party': 'Padaria',
                   'votes': encrypt(0, admin_pub_key)},

                  {'candidate_id': 1,
                   'name': 'Maria Ana',
                   'party': 'Partido Importante',
                   'votes': encrypt(0, admin_pub_key)},

                  {'candidate_id': 2,
                   'name': 'Peter Pan',
                   'party': 'Partido do Nunca',
                   'votes': encrypt(0, admin_pub_key)},

                  {'candidate_id': 3,
                   'name': 'Capitão Gancho',
                   'party': 'Piratas',
                   'votes': encrypt(0, admin_pub_key)}]
    dump(candidates, candidates_file)

    dump([], user_votes_file)  # As we do not have any user votes yet.


def vote(cpf: int, candidate: int, public_key: PaillierPublicKey):
    votes = load(user_votes_file)

    for v in votes:
        if v.get('CPF') == cpf:
            return True, 'You have already voted. Please, unvote first.\n'

    registry = encrypt(candidate, public_key)
    user_vote = {'CPF': cpf, 'encrypted_candidate_id': registry}

    if user_vote not in votes:
        dump_vote(
            user_vote,
            user_votes_file
        )

        candidates = load(candidates_file)

        for actual in candidates:
            if actual.get('candidate_id') == candidate:
                actual['votes'] += 1

                dump(candidates, candidates_file)
                return False, 'Vote confirmed.\n'


def unvote(voter_cpf: int, private_key: PaillierPrivateKey) -> dict:
    user_votes: list = load(user_votes_file)

    for user_vote in list(user_votes):
        if user_vote.get('CPF') == voter_cpf:
            encrypt_candidate = user_vote.get('encrypted_candidate_id')
            candidate: int = decrypt(encrypt_candidate, private_key)

            user_votes.remove(user_vote)

            dump(user_votes, user_votes_file)

            candidates = load(candidates_file)

            for actual in candidates:
                if actual.get('candidate_id') == candidate:
                    actual['votes'] -= 1

                    dump(candidates, candidates_file)

                    return actual


if __name__ == '__main__':
    key = private_key_from('1.txt')
    unvote(1, key)
