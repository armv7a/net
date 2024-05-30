import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import os
import subprocess
import shutil

def decrypt_aes_cbc(ciphertext_base64, key, iv):
    # 解码Base64
    ciphertext = base64.b64decode(ciphertext_base64)

    # 创建AES CBC解密器
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))

    # 解密数据并删除填充
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # 返回解密后的明文
    return decrypted_data.decode('utf-8')

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def files_are_equal(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

def main():
    # 替换为你的URL
    url = "https://gitlab.com/bobmolen/cloud/raw/master/vsp-cn.py"

    # 发送请求并获取密文
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch ciphertext from {url}. Status code: {response.status_code}")

    ciphertext_base64 = response.text.strip()

    # 替换为你的密钥和IV
    key = "36KeAARKZuKF39N9LFyycLUyKMhZDq0B"
    iv = "36KeAARKZuKF39N9"

    # 解密
    decrypted_text = decrypt_aes_cbc(ciphertext_base64, key, iv)

    # 写入到文件
    write_to_file("main.txt", decrypted_text)

    print("解密成功，已写入到 main.txt")

    # 检查 main.txt 和 tmp_main.txt 是否相同
    if files_are_equal('main.txt', 'tmp_main.txt'):
        print("main.txt 没有变更，不进行提交。")
    else:
        print("main.txt 有更新，提交到仓库...")
        shutil.copyfile('main.txt', 'tmp_main.txt')
        subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'])
        subprocess.run(['git', 'config', '--global', 'user.name', 'GitHub Actions'])
        subprocess.run(['git', 'add', 'main.txt', 'tmp_main.txt'])
        subprocess.run(['git', 'commit', '-m', 'Update main.txt and tmp_main.txt [skip ci]'])
        subprocess.run(['git', 'push'])

if __name__ == "__main__":
    main()
