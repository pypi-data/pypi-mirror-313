from .. import utils

class server_middleware:
    def __init__(self, secret = None):
        """密钥中间件

        Args:
            SECRET (str): 密钥
        """
        self.secret = secret # 解析密钥
        # 启用状态
        self.enabled = bool(secret)

    def apply_send(self, data):
        """加密数据"""
        # 未加密
        if not data.get("tunnel_encrypted", True) or not self.enabled: 
            data["data"]+=b'unencrypted;' 
            return data
        # 加密
        data["data"]=utils.aes_encrypt(data["data"], utils.calc_secret(self.secret, data["secret_id"]))
        return data

    def apply_recv(self, data):
        """解密数据"""
        # 未加密
        if data["data"][-12:] == b'unencrypted;': 
            data["data"] = data["data"][:-12]
            data["tunnel_encrypted"] = False   
            return data 
        # 服务端
        data["tunnel_encrypted"] = True
        # 计算密钥并解密
        data["secret_id"]=data["data"][-9:-1].decode()
        data["data"]=data["data"][:-10]
        data["data"]=utils.aes_decrypt(data["data"], utils.calc_secret(self.secret, data["secret_id"]))
        return data
    
class client_middleware:
    def __init__(self, secret = None):
        """密钥中间件

        Args:
            SECRET (str): 密钥
        """
        self.secret_id,self.secret,self.secret_md5,self.KEY_ID = utils.parse_secret(secret) # 解析密钥
        # 启用状态
        self.enabled = bool(secret)

    def apply_send(self, data):
        """加密数据"""
        # 未加密
        if not data.get("tunnel_encrypted", True) or (not self.enabled and not data.get("secret", False)): 
            data["data"]+=b'unencrypted;' 
            return data
        # 加密
        data["data"]=utils.aes_encrypt(data["data"], self.secret)+b';'+self.secret_id.encode()+b';' # 添加加密标记
        return data

    def apply_recv(self, data):
        """解密数据"""
        # 未加密
        if data["data"][-12:] == b'unencrypted;': 
            data["data"] = data["data"][:-12]
            data["tunnel_encrypted"] = False   
            return data 
        # 客户端
        if self.enabled:
            data["data"]=utils.aes_decrypt(data["data"], self.secret)
            return data
        else:
            raise Exception("Encrypted data received but no secret provided.")