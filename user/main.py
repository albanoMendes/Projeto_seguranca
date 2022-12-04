from src.database import candidates, vote
from tabulate import tabulate
from phe.paillier import generate_paillier_keypair
import src.key_store as key_store
from src.crypto import encrypt, decrypt


if __name__ == '__main__':
    print('Welcome. What would you like to do?\n')

    while True:
        options = ((0, 'Vote'), (1, 'Unvote'), (2, 'Exit'))
        print(tabulate(options, headers=['Options']))
        print()

        entry = int(input('? '))

        match entry:
            case 0:
                table = candidates()
                print(tabulate(table, headers=['ID', 'Name', 'Party']))
                print()

                cpf = int(input('Please type your CPF: '))

                candidate_id = int(input('Please type the desired candidate number: '))

                print('A key pair will be generated to testify the existence of your vote.\n')

                print('Your private key will be stored in a file named after your CPF.')
                print('Your public key will be used to encrypt your vote.\n')

                filename = '{}.txt'.format(cpf)

                public_key, private_key = generate_paillier_keypair()

                key_store.store(private_key, filename)

                vote(cpf, candidate_id, public_key)

                print('Vote confirmed')
            case 1:
                pass
            case 2:
                print('Have a good day.')
                exit(0)
            case _:
                print('Unknown option. Please choose between 0, 1 or 2.')
