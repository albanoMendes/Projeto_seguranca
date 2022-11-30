from database import candidates, vote
from tabulate import tabulate


if __name__ == '__main__':
    print('Would you like to vote?')
    print()

    table = candidates()
    print(tabulate(table, headers=['ID', 'Name', 'Party']))
    print()

    cpf = int(input('Please type your CPF: '))

    candidate_id = int(input('Please type the desired candidate number: '))

    vote(cpf, candidate_id)
