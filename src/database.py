# import mysql.connector
# import mysql.connector.cursor
from phe import PaillierPublicKey, PaillierPrivateKey
from src.crypto import encrypt, decrypt
from src.key_store import private_key_from
from admin.keystore import admin_pub_key, admin_priv_key
from __init__ import resource_dir
import dao

# connector = mysql.connector.connect(host='localhost', database='registry', user='root', password='password')
# cursor = connector.cursor()

candidatesFile = resource_dir / "candidates.pkl"
userVotesFile = resource_dir / "userVotes.pkl"
urnVotesFile = resource_dir / "urnVotes.pkl"
# Candidate  = [{"candidateId": int, "name": str, "party": str}] | primaryKey = candidateId
# UserVote = [{"cpf": str, "encryptedCandidateID": str}] | primaryKey = CPF
# UrnVote = [{"candidateID": int, "votes": str}] | primaryKey = candidateID


def insert_data():
    dao.insert({"candidateId": 0, "name": "Zé da Padaria", "party": "Padaria"},
               "candidateId",
               0,
               "candidates.pkl")
    dao.insert({"candidateId": 1, "name": "Maria Ana", "party": "Partido Importante"},
               "candidateId",
               1,
               "candidates.pkl")
    dao.insert({"candidateId": 2, "name": "Peter Pan", "party": "Partido do Nunca"},
               "candidateId",
               2,
               "candidates.pkl")
    dao.insert({"candidateId": 3, "name": "Capitão Gancho", "party": "Piratas"},
               "candidateId",
               3,
               "candidates.pkl")

    dao.insert({"candidateID": 0, "votes": encrypt(0, admin_pub_key)}, "candidateId", 0, "urnVotes.pkl")
    dao.insert({"candidateID": 1, "votes": encrypt(0, admin_pub_key)}, "candidateId", 1, "urnVotes.pkl")
    dao.insert({"candidateID": 2, "votes": encrypt(0, admin_pub_key)}, "candidateId", 2, "urnVotes.pkl")
    dao.insert({"candidateID": 3, "votes": encrypt(0, admin_pub_key)}, "candidateId", 3, "urnVotes.pkl")


def vote(cpf: int, candidate: int, public_key: PaillierPublicKey):
    user_vote = encrypt(candidate, public_key)
    user_vote = str(user_vote)

    # query = 'INSERT INTO UserVote (CPF, encriptedCandidateID) VALUES ({}, {!a});'.format(cpf, user_vote)
    # cursor.execute(query)
    # Pickle
    dao.insert({"cpf": cpf, "encryptedCandidateID": user_vote}, "CPF", cpf, userVotesFile)

    # query = 'SELECT votes FROM UrnVote WHERE candidateID = {}'.format(candidate)
    # cursor.execute(query)
    #
    # votes: tuple = cursor.fetchone()  # As a list of tuples...
    # votes: str = votes[0]  # ... And from the tuple, we get...
    # votes: bytes = eval(votes)  # The first element, which are the votes.
    # Pickle
    candidateVotes = dao.get("candidateID", candidate, urnVotesFile)
    encryptVotes = candidateVotes["votes"]

    votes: int = decrypt(encryptVotes, admin_priv_key)

    votes += 1
    encryptVotes: bytes = encrypt(votes, admin_pub_key)
    # votes: str = str(encryptVotes)

    # query = 'UPDATE UrnVote SET votes = {!a} WHERE candidateID = {}'.format(votes, candidate)
    # cursor.execute(query)
    #
    # connector.commit()
    # Pickle
    dao.insert({"candidateID": candidate, "votes": encryptVotes}, "candidateID", candidate, urnVotesFile)


def unvote(voter_cpf: int, private_key: PaillierPrivateKey) -> tuple:
    # query = 'SELECT encriptedCandidateID FROM UserVote WHERE CPF = {};'.format(voter_cpf)
    # cursor.execute(query)
    #
    # candidate: tuple = cursor.fetchone()
    # Pickle
    userVote = dao.get("CPF", voter_cpf, userVotesFile)
    encryptCandidate = userVote["encryptedCandidateID"]

    # if not candidate:
    #     return tuple()
    #
    # candidate: str = candidate[0]
    # candidate: bytes = eval(candidate)
    candidate: int = decrypt(encryptCandidate, private_key)

    # query = 'SELECT votes FROM UrnVote WHERE candidateID = {}'.format(candidate)
    # cursor.execute(query)
    # Pickle
    candidateVotes = dao.get("candidateID", candidate, urnVotesFile)
    encryptVotes = candidateVotes["votes"]

    votes: int = decrypt(encryptVotes, admin_priv_key)
    votes -= 1
    encryptVotes: bytes = encrypt(votes, admin_pub_key)

    # votes: tuple = cursor.fetchone()  # As a list of tuples...
    # votes: str = votes[0]  # ... And from the tuple, we get...
    # votes: bytes = eval(votes)  # The first element, which are the votes.
    # votes: int = decrypt(votes, admin_priv_key)
    # votes -= 1
    # votes: bytes = encrypt(votes, admin_pub_key)
    # votes: str = str(votes)

    # query = 'UPDATE UrnVote SET votes = {!a} WHERE candidateID = {}'.format(votes, candidate)
    # cursor.execute(query)
    #
    # connector.commit()
    # Pickle
    dao.insert({"candidateID": candidate, "votes": encryptVotes}, "candidateID", candidate, urnVotesFile)

    # query = 'SELECT name, party FROM Candidate WHERE candidateID = {}'.format(candidate)
    # cursor.execute(query)
    #
    # result = cursor.fetchone()
    # Pickle
    candidateVoted = dao.get("candidateID", candidate, candidatesFile)
    return candidateVoted


if __name__ == '__main__':
    insert_data()
    key = private_key_from('1.txt')
    unvote(1, key)
