from Crypto.Cipher import AES
from base64 import b64decode

# 密钥和 IV
key = b"36KeAARKZuKF39N9LFyycLUyKMhZDq0B"
iv = b"36KeAARKZuKF39N9"

# 打开 Base64 编码的加密文件
with open("vsp-cn.py", "r") as f:
    encrypted_base64_data = f.read()

# 先解码 Base64
encrypted_data = b64decode(encrypted_base64_data)

# 创建 AES 解密器
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(encrypted_data)

# 去除 PKCS5Padding
pad_len = decrypted_data[-1]
decrypted_data = decrypted_data[:-pad_len]

# 保存解密后的内容到 main.txt
with open("main.txt", "wb") as f:
    f.write(decrypted_data)
