import json
import threading
from . import adapter
from . import middleware
from . import plugin

class Server:
    def __init__(self,ID,SECRET,DESCRIPTION="",addresses=["tcp://0.0.0.0:10000"]):
        """初始化
        """
        # 设备ID
        self.ID=ID
        # 设备密钥
        self.SECRET=SECRET
        # 设备描述
        self.DESCRIPTION=DESCRIPTION
        # 地址
        self.addresses=addresses
        # 适配器
        self.adapter=adapter.manager.AdapterManager([adapter.parse_address("server",i) for i in addresses])
        # 函数挂载表
        self.mount_map={}
        # 加载插件
        plugin.server.manager.PluginManager(self).load([plugin.server.sys])
        # 运行状态
        self.running=False
        
    def mount(self,path,pack=True):
        """把函数挂载到连接
        Args:
            path (str): 挂载路径
            pack (bool, optional): 是否打包输入输出. Defaults to True.
        """
        def mount_decorator(func):
            self.mount_map[path]={
                "id":len(self.mount_map),
                "function":func,
                "path":path,
                "name":func.__name__,
                "pack":pack,
                "doc":func.__doc__
            }
            return func
        return mount_decorator

    # 设置适配器
    def init_adapters(self):
        """设置适配器
        """
        self.adapter.start()
    
    def init_middlewares(self):
        """设置中间件
        """
        # 如果adapter不存在
        if not hasattr(self,"adapter"):
            raise Exception("Adapter not set.")
        # 初始化中间件
        self.middlewares=[middleware.access.server_middleware(list(self.mount_map.keys()),secret=self.SECRET),
                            middleware.pack.middleware(),
                            middleware.encrypt.server_middleware(secret=self.SECRET),
                            middleware.checksum.middleware()]
        self.connection=middleware.manager.MiddlewareManager(adapter=self.adapter,middlewares=self.middlewares)
    
    def start(self):
        """运行服务
        """
        # 初始化适配器
        self.init_adapters()
        self.init_middlewares()
        # 检测是否建立连接
        if not hasattr(self,"connection"):
            raise Exception("Connection not established.")
        # 启动服务
        print(f"Server started.")
        print(f"Adapter Num:{len(self.adapter.adapters)}")
        print(f"Middleware Num:{len(self.middlewares)}")
        print(f"Mount Num:{len(self.mount_map)}")
        # 运行状态
        self.running=True
        while True:
            data=self.connection.recv(True)
            if not data: continue
            t=threading.Thread(target=self.handle_request,args=(data,))
            t.daemon=True
            t.start()
            
    def stop(self):
        """停止服务
        """
        self.adapter.stop()
        self.running=False
        return self
    
    def handle_request(self,data):
        if "id" in data["data"]: 
            data_copy=json.loads(json.dumps(data))
            data_copy["data"]={"id":data["data"]["id"],"status":"processing"}
            self.connection.send(data_copy)
        function=data["data"]["function"]
        params=data["data"]["params"]
        data["data"]={"id":data["data"]["id"],"function":data["data"]["function"]}
        try:
            res=self.execute(self.mount_map[function],params)
            data["data"]["result"]=res
        except Exception as e:
            data["data"]["err"]=str(e)
        self.connection.send(data)
        
    def execute(self,function,params):
        """执行函数
        """
        if function["pack"]:
            return function["function"](params)
        else:
            text="function[\"function\"]("
            for i in params:
                text+=f"{i}=params[\"{i}\"],"
            if text[-1]==',': text=text[:-1]
            text+=")"
            res=eval(text)
            if type(res)==tuple: res=list(res)
            if type(res)!=list: res=[res]
            return res
        
