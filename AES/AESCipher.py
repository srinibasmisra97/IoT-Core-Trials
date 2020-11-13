import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode


class AESCipher(object):

    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text)-1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)


if __name__ == '__main__':
    key = input("Enter AES Key: ")
    aes = AESCipher(key=key)

    choice = input("Enter E to encrypt and D to decrypt: ")
    if choice == "E":
        data = input("Enter data to encrypt: ")
        print("Encrypted Data: \n{}\n".format(aes.encrypt(plain_text=data)))
    elif choice == "D":
        data = input("Enter data to decrypt: ")
        print("Decrypted Data: \n{}\n".format(aes.decrypt(encrypted_text=data)))
    else:
        print("INVALID CHOICE")