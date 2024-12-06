import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import uuid

def aes_encrypt(data, key):
    aes = AES.new(key.encode(), AES.MODE_ECB)
    return aes.encrypt(pad(data, 16, 'pkcs7'))

def aes_decrypt(data, key):
    aes = AES.new(key.encode(), AES.MODE_ECB)
    return unpad(aes.decrypt(data), 16, 'pkcs7')

def md5(data):
    if type(data) == bytes:
        return hashlib.md5(data).hexdigest()
    return hashlib.md5(data.encode()).hexdigest()

def base64_encode(data):
    if type(data) == bytes:
        return base64.b64encode(data).decode()
    return base64.b64encode(data.encode()).decode()

def base64_decode(data):
    if type(data) == bytes:
        return base64.b64decode(data).decode()
    return base64.b64decode(data.encode()).decode()

def raw2acc(raw):
    """将权限字符串转换为权限代码
    """
    raw=raw[::-1] # 转换到倒序
    while len(raw)%8!=0:
        raw='0'+raw
    acc=""
    for i in range(0,len(raw),8):
        acc+=chr(int(raw[i:i+8],2))
    return base64_encode(acc)
    
def acc2raw(acc):
    """将权限代码转换为权限字符串
    """
    # 
    t=base64_decode(acc)
    raw=""
    for i in t:
        raw+=f"{ord(i):08b}"
    raw=raw[::-1] # 转换到正序
    return raw

def generate_device():
    """生成设备

    Returns:
        str: 生成的ID
        str: 生成的密钥
    """
    id = uuid.uuid4().hex
    secret = uuid.uuid4().hex
    return id,secret

def generate_acc(all_funcs:list,funcs:list):
    """生成权限代码

    Args:
        all_funcs (list): 所有函数
        funcs (list): 允许的函数

    Returns:
        str: 生成的权限代码
    """
    acc=""
    for i in all_funcs:
        if i in funcs:
            acc+="1"
        else:
            acc+="0"
    return raw2acc(acc)

def generate_secret(origin_secret, acc):
    """生成密钥

    Args:
        origin_secret (str): 服务端原始密钥
        acc (str): 权限代码

    Returns:
        str: 生成的密钥
    """
    # 八位随机密钥ID
    secret_id = uuid.uuid4().hex[:8]
    # 生成密钥
    secret=md5(f"{origin_secret}|{secret_id}")
    # 生成权限代码校验值
    acc_md5=md5(f"{origin_secret}|{secret_id}|{acc}")[:8]
    # 返回密钥
    return f"{secret_id}|{secret}|{acc}|{acc_md5}"

def calc_secret(origin_secret, secret_id):
    """计算密钥

    Args:
        origin_secret (str): 服务端原始密钥
        secret_id (str): 密钥ID

    Returns:
        str: 生成的密钥
    """
    return md5(f"{origin_secret}|{secret_id}")

def check_secret_valid(secret):
    """检查密钥是否有效

    Args:
        secret (str): 密钥

    Returns:
        bool: 是否有效
    """
    return secret.count("|")==3

def parse_secret(secret):
    """解析密钥

    Args:
        secret (str): 密钥

    Returns:
        str: 密钥ID
        str: 密钥
        str: 权限代码
        str: 权限代码校验值 
    """
    secret_id,secret,acc,acc_md5=secret.split("|")
    return secret_id,secret,acc,acc_md5

def check_secret(secret_id,secret,acc,acc_md5,origin_secret):
    """校验密钥

    Args:
        secret_id (str): 密钥ID
        secret (str): 密钥
        acc (str): 权限代码
        acc_md5 (str): 权限代码校验值
        origin_secret (str): 服务端原始密钥

    Returns:
        bool: 是否校验通过
    """
    return secret==md5(f"{origin_secret}|{secret_id}") and acc_md5==md5(f"{origin_secret}|{secret_id}|{acc}")[:8]

def check_func_auth(funcs, func, acc):
    """检查函数是否授权

    Args:
        func (str): 函数名
        acc (str): 权限代码

    Returns:
        bool: 是否授权
    """
    acc=acc2raw(acc) # 将acc转换为二进制模式
    function_authorized=False
    while True:
        # 逐级检查权限
        if func in funcs and acc[funcs.index(func)]=='1':
            function_authorized=True
            break
        if '.' not in func:
            break
        func=func[:func.rindex('.')]
    return function_authorized

