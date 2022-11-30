import mysql.connector
import mysql.connector.cursor


connector = mysql.connector.connect(host='localhost', database='registry', user='root', password='password')


def vote(cpf, candidate):
    sql = f'INSERT INTO Vote (CPF, candidateID) VALUES ({cpf}, {candidate});'
    cursor = connector.cursor()
    cursor.execute(sql)
    connector.commit()


def candidates():
    sql = f'SELECT * FROM Candidate'
    cursor = connector.cursor()
    cursor.execute(sql)

    result = [result for result in cursor]
    return result


def vote_from(voter_cpf) -> str:
    sql = f"""SELECT c.name 
              FROM Candidate c 
              WHERE c.candidateID = (SELECT v.candidateID FROM Vote v WHERE v.CPF = {voter_cpf});"""
    cursor = connector.cursor()
    cursor.execute(sql)

    result = [result for result in cursor]  # Retrieves possible results from the cursor.
    result = result.pop()  # Gets the first item, at position 0, which will be a tuple.

    return result[0]  # Returns the first position of the tuple - the candidate's name.


if __name__ == '__main__':
    print(candidates())
