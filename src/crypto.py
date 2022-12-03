from phe import paillier, EncodedNumber


num1 = 10
num2 = 20

pub_key, priv_key = paillier.generate_paillier_keypair()
p1, p2 = paillier.generate_paillier_keypair()
print(p1 == pub_key)

cipher_num1, cipher_num2 = pub_key.encrypt(num1), pub_key.encrypt(num2)
print(cipher_num1)

# add two encrypted numbers together
result = cipher_num1 + cipher_num2
result = priv_key.decrypt(result)
print("add two encrypted numbers together:", result)

# add an encrypted number to a plaintext number
result = cipher_num1 + 5
result = priv_key.decrypt(result)
print("add an encrypted number to a number:", result)

# multiply an encrypted number by a plaintext number
result = cipher_num1 * 10
result = priv_key.decrypt(result)
print("multiply an encrypted number to a number:", result)
