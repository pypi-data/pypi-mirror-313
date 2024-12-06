class PluginManager:
    def __init__(self, server):
        """ 插件管理器
        
        Args:
            Server: 连接对象
        """
        self.server = server
        
    def load(self,plugins):
        """ 加载插件
        """
        for plugin in plugins:
            print(f"Loading plugin {plugin.__name__}.")
            plugin.plugin(self.server).load()