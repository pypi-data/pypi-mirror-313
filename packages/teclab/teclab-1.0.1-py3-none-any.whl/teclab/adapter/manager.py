class AdapterManager:
    """适配器管理器"""
    def __init__(self, adapters=None):
        self.adapters = adapters or []
        self.recv_cache = []
        
    def add_adapter(self, adapter):
        """添加适配器"""
        self.adapters.append(adapter)
    
    def remove_adapter(self, adapter):
        """移除适配器"""
        self.adapters.remove(adapter)
    
    def recv(self, block=False):
        """接收数据
        Args:
            block: 是否阻塞
        """
        while not self.recv_cache:
            for adapter in self.adapters:
                res=adapter.recv(block)
                if res: 
                    res["channel"]=str(self.adapters.index(adapter))+'-'+str(res["channel"])
                    self.recv_cache.append(res)
            if not block:
                break
        return self.recv_cache.pop(0) if len(self.recv_cache)>0 else False

    def send(self, data, block=True):
        """发送数据
        Args:
            data: 数据
            block: 是否阻塞
        """
        if "channel" not in data: data["channel"]="0-0"
        id=int(data["channel"].split('-')[0])
        data["channel"]=int(data["channel"].split('-')[1])
        self.adapters[id].send(data=data, block=block)
        return True
        
        
        