import mysql.connector
import mysql.connector.cursor


connector = mysql.connector.connect(host='localhost', database='registry', user='root', password='password')


def vote(cpf, candidate):
    query = f'INSERT INTO Vote (CPF, candidateID) VALUES ({cpf}, {candidate});'
    cursor = connector.cursor()
    cursor.execute(query)
    connector.commit()


def candidates():
    query = f'SELECT * FROM Candidate'
    cursor = connector.cursor()
    cursor.execute(query)

    result = [result for result in cursor]
    return result


def retrieve_votes():
    query = 'SELECT candidateID, c.name, COUNT(candidateID) FROM Vote GROUP BY candidateID'
    cursor = connector.cursor()
    cursor.execute(query)

    result = [result for result in cursor]
    return result


def vote_from(voter_cpf) -> str:
    query = f"""SELECT c.name 
              FROM Candidate c 
              WHERE c.candidateID = (SELECT v.candidateID FROM Vote v WHERE v.CPF = {voter_cpf});"""
    cursor = connector.cursor()
    cursor.execute(query)

    result = [result for result in cursor]  # Retrieves possible results from the cursor.
    result = result.pop()  # Gets the first item, at position 0, which will be a tuple.

    return result[0]  # Returns the first position of the tuple - the candidate's name.


if __name__ == '__main__':
    print(retrieve_votes())
