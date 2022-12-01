from pickle import dump, load
from phe.paillier import PaillierPrivateKey, generate_paillier_keypair
from __init__ import resource_dir


def store(key: PaillierPrivateKey, filename):
    with open(resource_dir / filename, 'wb') as f:
        dump(key, f)


def private_key_from(filename):
    with open(resource_dir / filename, 'rb') as f:
        return load(f)


if __name__ == '__main__':
    _, pv_key = generate_paillier_keypair()
    store(pv_key, 'stub_pv_key.txt')

    pv_key2 = private_key_from('stub_pv_key.txt')
    print(pv_key == pv_key2)  # Must return True.
