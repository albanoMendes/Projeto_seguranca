from src.database import vote, unvote
from admin.database import candidates
from tabulate import tabulate
from phe.paillier import generate_paillier_keypair
import src.key_store as key_store


if __name__ == '__main__':
    print('Welcome.\n')

    print('Identify yourself. Please type your CPF. ')
    cpf = int(input('? '))

    print('What would you like to do?\n')

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

                print('Please type the desired candidate number.')
                candidate_id = int(input('? '))
                print()

                print('A key pair will be generated to testify the existence of your vote.\n')

                print('Your private key will be stored in a file named after your CPF.')
                print('Your public key will be used to encrypt your vote.\n')

                filename = '{}.txt'.format(cpf)

                public_key, private_key = generate_paillier_keypair()

                key_store.store(private_key, filename)

                vote(cpf, candidate_id, public_key)

                print('Vote confirmed.\n')
            case 1:
                filename = '{}.txt'.format(cpf)
                private_key = key_store.private_key_from(filename)

                vote = unvote(cpf, private_key)

                if vote:
                    print('You have voted for {} of {}\n'.format(vote["name"], vote["party"]))
                else:
                    print('You did not vote yet.\n')
            case 2:
                print('Have a good day.')
                exit(0)
            case _:
                print('Unknown option. Please choose between 0, 1 or 2.')
