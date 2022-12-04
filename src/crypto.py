from phe import PaillierPublicKey, PaillierPrivateKey
from pickle import dumps, loads


def encrypt(vote: int, public_key: PaillierPublicKey) -> bytes:
    vote = public_key.encrypt(vote)
    return dumps(vote)


def decrypt(vote: bytes, private_key: PaillierPrivateKey) -> int:
    vote = loads(vote)
    return private_key.decrypt(vote)
