import time
from . import adapter
from . import middleware
from . import plugin
import uuid

class Client:
    def __init__(self,adapter_,middlewares=None,SECRET=None):
        # 参数
        self.adapter=adapter_
        self.SECRET=SECRET
        # 构建连接
        self.middlewares=middlewares if middlewares is not None else [middleware.access.client_middleware(secret=self.SECRET),
                                                                      middleware.pack.middleware(),
                                                                      middleware.encrypt.client_middleware(self.SECRET),
                                                                      middleware.checksum.middleware()]
        self.connection=middleware.manager.MiddlewareManager(adapter=adapter.manager.AdapterManager(adapters=[self.adapter]),middlewares=self.middlewares)

    def request(self,function,params,auto_retry=True,confirm_timeout=3,result_timeout=30):
        id=str(uuid.uuid4())
        # 发送请求
        self.connection.send({"id":id,"function":function,"params":params},block=True) 
        # 等待响应
        send_time=time.time()
        confirmed=False
        while time.time()-send_time<confirm_timeout:
            res=self.connection.recv(block=False)
            if res and res["data"]["id"]==id and res["data"]["status"]=="processing":
                confirmed=True
                confirm_time=time.time()
                break
            time.sleep(0.01)
        if not confirmed:
            if auto_retry: return self.request(function,params,auto_retry)
            raise Exception("Request timeout.")
        # 返回结果
        while time.time()-confirm_time<result_timeout:
            res=self.connection.recv(block=True)
            if res["data"]["id"]==id and res["data"].get("result") is not None:
                return True,res["data"]["result"]
            if res["data"]["id"]==id and res["data"].get("err") is not None:
                return False,res["data"]["err"]
            time.sleep(0.01)
        raise Exception("Result timeout.")
