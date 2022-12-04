from phe import paillier, PaillierPublicKey, PaillierPrivateKey
from pickle import dumps, loads
from base64 import b64encode, b64decode


def encrypt(vote: int, public_key: PaillierPublicKey) -> bytes:
    vote = public_key.encrypt(vote)
    vote = dumps(vote)
    return b64encode(vote)


def decrypt(vote: bytes, private_key: PaillierPrivateKey) -> int:
    vote = b64decode(vote)
    vote = loads(vote)
    return private_key.decrypt(vote)

