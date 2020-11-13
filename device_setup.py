import requests
import random
import string
import json

from AES.AESCipher import AESCipher
from RSA.RSACipher import RSACipher
from DeviceManagement.Manager import DeviceManager

DEVICE_ID = "device-0"

if __name__ == '__main__':
    RSAObject = RSACipher()
    RSAObject.set_public_key(public_key_file="keys/RSA/public.pem")

    print("ENCRYPTION IN PROGRESS!")
    aes_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
    encrypted_key = RSAObject.encrypt(plain_text=aes_key)
    print("AES Key: {}\n".format(encrypted_key))

    AESObject = AESCipher(key=aes_key)
    encrypted_public_key_file = AESObject.encrypt(plain_text=open("keys/public_key.pub", 'r').read())
    print("Encrypted Public Key File: \n{}\n".format(encrypted_public_key_file))

    response = requests.post(url="http://localhost:5000/device", json={
        "id": DEVICE_ID,
        "key": encrypted_public_key_file,
        "secret": encrypted_key
    })

    print(response.status_code)