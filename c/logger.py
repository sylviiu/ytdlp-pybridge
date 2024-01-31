class Logger:
    def __init__(self, wsHook):
        self.wsHook = wsHook
    
    def debug(self, msg):
        self.wsHook.debug(msg)
    
    def info(self, msg):
        pass

    def warning(self, msg):
        self.wsHook.warning(msg)
    
    def error(self, msg):
        self.wsHook.error(msg)