class MiddlewareManager:
    def __init__(self, adapter, middlewares=[]):
        """ 中间件管理器
        
        Args:
            adapter: 适配器管理器
            middlewares: 中间件(发送顺序)
        """
        self.adapter = adapter
        self.middlewares = middlewares 
        
    def add_middleware(self, middleware):
        """添加中间件"""
        self.middlewares.append(middleware)
    
    def remove_middleware(self, middleware):
        """移除中间件"""
        self.middlewares.remove(middleware)
    
    def apply_send_middleware(self, data):
        """处理发送数据的中间件"""
        for middleware in self.middlewares:
            data = middleware.apply_send(data)
            if not data:
                return False
        return data

    def apply_recv_middleware(self, data):
        """处理接收数据的中间件"""
        for middleware in self.middlewares[::-1]:
            data = middleware.apply_recv(data)
            if not data:
                return False
        return data
    
    def recv(self, block=False):
        """接收数据
        Args:
            block: 是否阻塞
        """
        while True:
            res = self.adapter.recv(block)
            if res:
                res = self.apply_recv_middleware(res)
                return res
            if not block:
                break
        return False
    
    def send(self, data, block=True):
        """发送数据
        Args:
            data: 数据
            block: 是否阻塞
        """
        data = self.apply_send_middleware(data)
        self.adapter.send(data=data, block=block)
        return True