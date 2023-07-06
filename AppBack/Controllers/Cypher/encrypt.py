import base64
import json
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
from rest_framework.renderers import BaseRenderer

load_dotenv()

# here the string gotten from the environmental variable is converted to bytes
AES_SECRET_KEY = bytes(os.getenv("AES_SECRET_KEY"), "utf-8")
AES_IV = bytes(os.getenv("AES_IV"), "utf-8")


class CustomAesRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "aes"

    def render(self, data, media_type=None, renderer_context=None):
        plaintext = json.dumps(data)
        padded_plaintext = pad(plaintext.encode(), AES.block_size)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)  # NOSONAR
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        response = {"ciphertext": ciphertext_b64}
        return json.dumps(response)

    def decryptJson(self, data):
        ciphertext = base64.b64decode(data["ciphertext"])
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)  # NOSONAR
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        plaintext_text = plaintext.decode("utf-8")
        return json.loads(plaintext_text)

    def encryptString(self, data):
        padded_plaintext = pad(data.encode(), AES.block_size)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)  # NOSONAR
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        return ciphertext_b64

    def decryptString(self, data):
        ciphertext = base64.b64decode(data)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)  # NOSONAR
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        plaintext_text = plaintext.decode("utf-8")
        return plaintext_text
