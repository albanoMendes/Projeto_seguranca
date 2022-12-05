from os.path import isfile
from pickle import dump, load
from phe.paillier import generate_paillier_keypair


def keys():
    if not isfile('admin/keyring'):
        with open('admin/keyring', 'wb') as keyring:
            public_key, private_key = generate_paillier_keypair()
            dump((public_key, private_key), keyring)

    with open('admin/keyring', 'rb') as keyring:
        public_key, private_key = load(keyring)

    return public_key, private_key


admin_pub_key, admin_priv_key = keys()


if __name__ == '__main__':
    print(admin_pub_key)
