


class plugin:
    def __init__(self, server):
        """ 提供系统函数
        """
        self.server = server
        
    def load(self):
        """ 加载插件
        """
        @self.server.mount("sys")
        def sys(params):
            """系统基本信息
            """
            return info({})
        
        @self.server.mount("sys.info")
        def info(params):
            """系统基本信息

            Returns:
                id: 设备ID
                description: 设备描述
            """
            return {"id":self.server.ID,"description":self.server.DESCRIPTION}
    
        @self.server.mount("sys.echo")
        def echo(params):
            """Echo text

            Args:
                text (str): Text to echo

            Returns:
                text: Echoed text
            """
            return {"text":params["text"]}
        
        @self.server.mount("sys.error",pack=False)
        def error(text):
            """Raise an exception

            Args:
                text (str): Error message

            Raises:
                Exception: text
            """
            raise Exception(text)
        
        @self.server.mount("sys.list",pack=False)
        def list_funcs(detail:bool=False):
            """列出所有函数

            Args:
                detail (bool): 是否显示详细信息
                
            Returns:
                list: 函数列表
            """
            if not detail: return list(self.server.mount_map.keys()) 
            res=[]
            for path in self.server.mount_map:
                res.append({
                    "id":self.server.mount_map[path]["id"],
                    "path":self.server.mount_map[path]["path"],
                    "doc":self.server.mount_map[path]["doc"]
                })
            return res
        
        @self.server.mount("sys.manual",pack=False)
        def manual(path):
            """获取函数文档

            Args:
                path (str): 函数挂载路径

            Raises:
                Exception: 未找到函数

            Returns:
                str: 函数文档
            """
            if path not in self.server.mount_map:
                raise Exception("Manual: Function not found.")
            return self.server.mount_map[path]["doc"]
        
        