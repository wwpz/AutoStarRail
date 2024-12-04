from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64


class AESCipher:
    def __init__(self, password: str, salt: bytes = None):
        # 如果没有提供盐值，则生成一个随机盐值
        self.salt = salt if salt else get_random_bytes(16)
        # 派生密钥
        self.key = self._derive_key(password, self.salt)

    def _derive_key(self, password: str, salt: bytes, key_length: int = 32) -> bytes:
        # 使用 PBKDF2 算法从密码和盐值派生一个密钥
        return PBKDF2(password, salt, dkLen=key_length, count=100000)

    def encrypt(self, plaintext: str) -> str:
        # 创建一个新的 AES 加密对象，使用 GCM 模式
        cipher = AES.new(self.key, AES.MODE_GCM)
        # 加密数据，并生成消息认证码(tag)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
        # 将数据编码为 base64，以便安全地传输或存储
        result = base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
        return result

    def decrypt(self, enc: str) -> str:
        # 从 base64 解码数据
        data = base64.b64decode(enc)
        # 分离出 nonce, tag 和密文(ciphertext)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        # 重新创建 AES 加密对象，使用之前的 nonce
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        # 解密数据并验证其完整性
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')

# 用法示例
# password = 'my_very_secure_password'
# salt = get_random_bytes(16)  # 自定义盐值
# cipher = AESCipher(password, salt)
#
# plaintext = "This is a secret message."
# encrypted = cipher.encrypt(plaintext)
# print(f"Encrypted: {encrypted}")
#
# # 使用相同的密码和盐值进行解密
# cipher = AESCipher(password, salt)
# decrypted = cipher.decrypt(encrypted)
# print(f"Decrypted: {decrypted}")
