from src.database import candidates, vote
from tabulate import tabulate
from phe.paillier import generate_paillier_keypair
import src.key_store as key_store
import src.key_handler as key_handler


if __name__ == '__main__':
    print('Would you like to vote?\n')
    print()

    table = candidates()
    print(tabulate(table, headers=['ID', 'Name', 'Party']))
    print()

    cpf = int(input('Please type your CPF: '))

    candidate_id = int(input('Please type the desired candidate number: '))

    print('A key pair will be generated to testify the existence of your vote.\n')

    print('Your private key will be stored in a file named after your CPF.')
    print('Your public key will be used to encrypt your vote.')

    filename = f'{str(cpf)}.txt'

    public_key, private_key = generate_paillier_keypair()

    key_store.store(private_key, filename)

    digested_key = key_handler.encode(public_key)  # Digests to b64 to put into database.

    print(digested_key)
    vote(cpf, candidate_id)
