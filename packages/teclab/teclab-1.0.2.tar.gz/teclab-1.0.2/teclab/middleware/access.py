# 权限控制中间件
from .. import utils

class server_middleware:
    def __init__(self, function_map:list, secret:str):
        self.function_map = function_map
        self.secret = secret
        self.default_access_control_code="Bg==" # 默认权限控制代码
        
    def apply_recv(self, data):
        """权限控制中间件-接收
        """
        # 未授权
        data["authorized"]=False
        # 检查是否有函数名
        if (not "function" in data["data"]) or data["data"]["function"] not in self.function_map: return self.return_err(data,"Function not found!") # 返回错误信息
        # 是否携带密钥
        if not data["tunnel_encrypted"] or "secret" not in data["data"]:
            acc=self.default_access_control_code
        else:
            # 检查密钥是否有效
            client_secret=data["data"]["secret"]
            if not utils.check_secret_valid(client_secret): return self.return_err(data,"Secret invalid!") # 返回错误信息
            # 解析密钥
            secret_id,secret,acc,acc_md5=utils.parse_secret(client_secret)
            # 校验密钥
            if not utils.check_secret(secret_id,secret,acc,acc_md5,self.secret): return self.return_err(data,"Secret invalid!") # 返回错误信息
        # 检验函数是否授权
        if not utils.check_func_auth(self.function_map,data["data"]["function"],acc): return self.return_err(data,"Permission denied!") # 返回错误信息
        # 通过校验
        data["authorized"]=True
        return data

    def apply_send(self, data):
        """权限控制中间件-发送
        """
        # 不需要检查返回内容
        return data
    
    def return_err(self,data,err):
        # 返回错误信息
        data["data"]["function"]="sys.error"
        data["data"]["params"]={"text":err}
        return data
    
class client_middleware:
    def __init__(self, secret:str=None):
        self.secret = secret
        self.enable = bool(secret)
        
    def apply_send(self, data):
        # 添加权限信息
        if self.enable:
            data["secret"]=self.secret
        return data
    
    def apply_recv(self, data):
        # 不需要检查返回内容
        return data