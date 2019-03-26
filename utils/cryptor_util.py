# -*- coding: utf-8 -*-
from utils.RNCryptor import RNCryptor


class Crypto(object):
    """
    AES 加密算法简单包装，基本用法
    ```
    crypto = Crypto()
    crypto.configure(app.config)

    cipher_data = crypto.encrypt(b'hello, world!')
    plain_data = crypto.decrypt(cipher_data)
    ```

    see https://github.com/RNCryptor/RNCryptor
    """
    def __init__(self):
        self._config = {}
        self._config.setdefault('CRYPTO_KEY', b'\0'*16)

        self._crypto = RNCryptor()

    def configure(self, config=None, **kwargs):
        if config:
            self._config.update(config)
        if kwargs:
            self._config.update(kwargs)

    def encrypt(self, plain_data, iterations=10000):
        return self._crypto.encrypt(plain_data, self._config['CRYPTO_KEY'], iterations)

    def decrypt(self, cipher_data, iterations=10000):
        return self._crypto.decrypt(cipher_data, self._config['CRYPTO_KEY'], iterations)
