from base64 import b64encode, b64decode
from pickle import dumps, loads
from phe.paillier import PaillierPublicKey, generate_paillier_keypair


def encode(public_key: PaillierPublicKey) -> bytes:
    dumped = dumps(public_key)
    return b64encode(dumped)


def decode(public_key_bytes: bytes) -> PaillierPublicKey:
    decoded = b64decode(public_key_bytes)
    return loads(decoded)


if __name__ == '__main__':
    pb_key, _ = generate_paillier_keypair()

    encoded_key = encode(pb_key)
    decoded_key = decode(encoded_key)

    print(pb_key == decoded_key)  # Must return True.
