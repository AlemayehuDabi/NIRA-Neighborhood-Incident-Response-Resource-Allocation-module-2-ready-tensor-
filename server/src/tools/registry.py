class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, name:str, tool):
        self.tools[name] = tool
    
    def get(self, name):
        return self.tools.get(name)
    
    def all(self):
        return self.tools