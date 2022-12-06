from phe import PaillierPublicKey, PaillierPrivateKey
from phe.paillier import EncryptedNumber


def encrypt(vote: int, public_key: PaillierPublicKey) -> EncryptedNumber:
    return public_key.encrypt(vote)


def decrypt(vote: EncryptedNumber, private_key: PaillierPrivateKey) -> int:
    return private_key.decrypt(vote)
