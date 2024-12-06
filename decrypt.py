from Crypto.Cipher import AES

# 密钥和 IV
key = b"36KeAARKZuKF39N9LFyycLUyKMhZDq0B"
iv = b"36KeAARKZuKF39N9"

# 打开加密文件
with open("vsp-cn.py", "rb") as f:
    encrypted_data = f.read()

# 创建 AES 解密器
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(encrypted_data)

# 去除 PKCS5Padding
pad_len = decrypted_data[-1]
decrypted_data = decrypted_data[:-pad_len]

# 保存解密后的内容到 main.txt
with open("main.txt", "wb") as f:
    f.write(decrypted_data)
