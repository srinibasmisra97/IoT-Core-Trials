from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify


class RSACipher(object):

    def __init__(self):
        self.public_key = None
        self.private_key = None

    def set_public_key(self, public_key_file):
        self.public_key = RSA.importKey(open(public_key_file, 'r').read())

    def set_private_key(self, private_key_file):
        self.private_key = RSA.importKey(open(private_key_file, 'r').read())

    def encrypt(self, plain_text):
        if self.public_key is None:
            return None
        cipher = PKCS1_OAEP.new(key=self.public_key)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return hexlify(encrypted_text).decode()

    def decrypt(self, encrypted_text):
        if self.private_key is None:
            return None
        cipher = PKCS1_OAEP.new(key=self.private_key)
        decrypted_text = cipher.decrypt(unhexlify(encrypted_text))
        return decrypted_text.decode()


if __name__ == '__main__':
    RSAObject = RSACipher()
    RSAObject.set_private_key(private_key_file="../keys/RSA/private.pem")
    RSAObject.set_public_key(public_key_file="../keys/RSA/public.pem")

    choice = input("Enter E to encrypt and D to decrypt: ")
    if choice == "E":
        data = input("Enter plain text data: ")
        print("Encrypted Data: \n{}\n".format(RSAObject.encrypt(plain_text=data)))
    elif choice == "D":
        data = input("Enter encrypted data: ")
        print("Plain Text Data: \n{}\n".format(RSAObject.decrypt(encrypted_text=data)))
    else:
        print("CHOICE NOT RECOGNISED!")