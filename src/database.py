from phe import PaillierPublicKey, PaillierPrivateKey
from src.crypto import encrypt, decrypt
from src.key_store import private_key_from
from admin.key_store import admin_pub_key
from __init__ import resource_dir
from src.dao import insert, get, remove, dump
from os.path import isfile


candidatesFile = resource_dir / "candidates.pkl"
userVotesFile = resource_dir / "userVotes.pkl"
urnVotesFile = resource_dir / "urnVotes.pkl"


def insert_data():
    if isfile(candidatesFile) or isfile(userVotesFile) or isfile(urnVotesFile):
        return

    dump([], candidatesFile)
    dump([], userVotesFile)
    dump([], urnVotesFile)

    insert({"candidateId": 0, "name": "Zé da Padaria", "party": "Padaria"},
           "candidateId",
           0,
           candidatesFile)
    insert({"candidateId": 1, "name": "Maria Ana", "party": "Partido Importante"},
           "candidateId",
           1,
           candidatesFile)
    insert({"candidateId": 2, "name": "Peter Pan", "party": "Partido do Nunca"},
           "candidateId",
           2,
           candidatesFile)
    insert({"candidateId": 3, "name": "Capitão Gancho", "party": "Piratas"},
           "candidateId",
           3,
           candidatesFile)

    insert({"candidateId": 0, "votes": encrypt(0, admin_pub_key)}, "candidateId", 0, urnVotesFile)
    insert({"candidateId": 1, "votes": encrypt(0, admin_pub_key)}, "candidateId", 1, urnVotesFile)
    insert({"candidateId": 2, "votes": encrypt(0, admin_pub_key)}, "candidateId", 2, urnVotesFile)
    insert({"candidateId": 3, "votes": encrypt(0, admin_pub_key)}, "candidateId", 3, urnVotesFile)


def vote(cpf: int, candidate: int, public_key: PaillierPublicKey):
    user_vote = encrypt(candidate, public_key)

    if insert({"CPF": cpf, "encryptedCandidateID": user_vote}, "CPF", cpf, userVotesFile):
        candidateVotes = get("candidateId", candidate, urnVotesFile)
        encryptVotes = candidateVotes["votes"]

        insert({"candidateId": candidate, "votes": encryptVotes + 1}, "candidateId", candidate, urnVotesFile)
        return 'Vote confirmed.\n'
    else:
        return 'You have already voted. Please, unvote first.\n'


def unvote(voter_cpf: int, private_key: PaillierPrivateKey) -> tuple:
    userVote = get("CPF", voter_cpf, userVotesFile)
    encryptCandidate = userVote["encryptedCandidateID"]
    candidate: int = decrypt(encryptCandidate, private_key)
    remove("CPF", voter_cpf, userVotesFile)

    candidateVotes = get("candidateId", candidate, urnVotesFile)
    encryptVotes = candidateVotes["votes"]

    insert({"candidateId": candidate, "votes": encryptVotes - 1}, "candidateId", candidate, urnVotesFile)

    return get("candidateId", candidate, candidatesFile)


if __name__ == '__main__':
    key = private_key_from('1.txt')
    unvote(1, key)
