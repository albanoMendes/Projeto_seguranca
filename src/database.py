import mysql.connector
import mysql.connector.cursor
from phe import PaillierPublicKey, PaillierPrivateKey
from src.crypto import encrypt, decrypt
from src.key_store import private_key_from
from admin.keystore import admin_pub_key, admin_priv_key

connector = mysql.connector.connect(host='localhost', database='registry', user='root', password='password')
cursor = connector.cursor()


def vote(cpf: int, candidate: int, public_key: PaillierPublicKey):
    user_vote = encrypt(candidate, public_key)
    user_vote = str(user_vote)

    query = 'INSERT INTO UserVote (CPF, encriptedCandidateID) VALUES ({}, {!a});'.format(cpf, user_vote)
    cursor.execute(query)

    query = 'SELECT votes FROM UrnVote WHERE candidateID = {}'.format(candidate)
    cursor.execute(query)

    votes: tuple = cursor.fetchone()  # As a list of tuples...
    votes: str = votes[0]  # ... And from the tuple, we get...
    votes: bytes = eval(votes)  # The first element, which are the votes.

    if votes != 0:
        votes: int = decrypt(votes, admin_priv_key)

    votes += 1
    votes: bytes = encrypt(votes, admin_pub_key)
    votes: str = str(votes)

    query = 'UPDATE UrnVote SET votes = {!a} WHERE candidateID = {}'.format(votes, candidate)
    cursor.execute(query)

    connector.commit()


def unvote(voter_cpf: int, private_key: PaillierPrivateKey) -> tuple:
    query = 'SELECT encriptedCandidateID FROM UserVote WHERE CPF = {};'.format(voter_cpf)
    cursor.execute(query)

    candidate: tuple = cursor.fetchone()

    if not candidate:
        return tuple()

    candidate: str = candidate[0]
    candidate: bytes = eval(candidate)
    candidate: int = decrypt(candidate, private_key)

    query = 'SELECT votes FROM UrnVote WHERE candidateID = {}'.format(candidate)
    cursor.execute(query)

    votes: tuple = cursor.fetchone()  # As a list of tuples...
    votes: str = votes[0]  # ... And from the tuple, we get...
    votes: bytes = eval(votes)  # The first element, which are the votes.
    votes: int = decrypt(votes, admin_priv_key)
    votes -= 1
    votes: bytes = encrypt(votes, admin_pub_key)
    votes: str = str(votes)

    query = 'UPDATE UrnVote SET votes = {!a} WHERE candidateID = {}'.format(votes, candidate)
    cursor.execute(query)

    connector.commit()

    query = 'SELECT name, party FROM Candidate WHERE candidateID = {}'.format(candidate)
    cursor.execute(query)

    result = cursor.fetchone()
    return result


if __name__ == '__main__':
    key = private_key_from('1.txt')
    unvote(1, key)
