from phe import PaillierPublicKey, PaillierPrivateKey
from src.crypto import encrypt, decrypt
from src.key_store import private_key_from
from admin.keystore import admin_pub_key, admin_priv_key
from __init__ import resource_dir
from src.dao import insert, get, remove, __dump


candidatesFile = resource_dir / "candidates.pkl"
userVotesFile = resource_dir / "userVotes.pkl"
urnVotesFile = resource_dir / "urnVotes.pkl"


# Candidate  = [{"candidateId": int, "name": str, "party": str}] | primaryKey = candidateId
# UserVote = [{"CPF": str, "candidateId": str}] | primaryKey = CPF
# UrnVote = [{"candidateId": int, "votes": str}] | primaryKey = candidateId


def insert_data():
    __dump([], candidatesFile)
    __dump([], userVotesFile)
    __dump([], urnVotesFile)

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
    user_vote = user_vote
    insert({"CPF": cpf, "encryptedCandidateID": user_vote}, "CPF", cpf, userVotesFile)

    candidateVotes = get("candidateId", candidate, urnVotesFile)
    encryptVotes = candidateVotes["votes"]
    votes: int = decrypt(encryptVotes, admin_priv_key)
    votes += 1
    encryptVotes: bytes = encrypt(votes, admin_pub_key)
    insert({"candidateId": candidate, "votes": encryptVotes}, "candidateId", candidate, urnVotesFile)


def unvote(voter_cpf: int, private_key: PaillierPrivateKey) -> tuple:
    userVote = get("CPF", voter_cpf, userVotesFile)
    encryptCandidate = userVote["encryptedCandidateID"]
    candidate: int = decrypt(encryptCandidate, private_key)
    remove("CPF", voter_cpf, userVotesFile)

    candidateVotes = get("candidateId", candidate, urnVotesFile)
    encryptVotes = candidateVotes["votes"]
    votes: int = decrypt(encryptVotes, admin_priv_key)
    votes -= 1
    encryptVotes: bytes = encrypt(votes, admin_pub_key)
    insert({"candidateId": candidate, "votes": encryptVotes}, "candidateId", candidate, urnVotesFile)

    candidateVoted = get("candidateId", candidate, candidatesFile)
    return candidateVoted


if __name__ == '__main__':
    key = private_key_from('1.txt')
    unvote(1, key)
