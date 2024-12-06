class PluginManager:
    def __init__(self, client):
        """ 插件管理器
        
        Args:
            Client: 连接对象
        """
        self.client = client
        
    def load(self,plugins):
        """ 加载插件
        """
        for plugin in plugins:
            print(f"Loading plugin {plugin.__name__}.")
            plugin.plugin(self.client).load()