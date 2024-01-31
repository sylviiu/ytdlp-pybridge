import re

class Logger:
    def __init__(self, wsHook, debugsToError=False):
        self.wsHook = wsHook
        self.debugsToError = debugsToError
    
    def debug(self, msg):
        # https://github.com/yt-dlp/yt-dlp#adding-logger-and-progress-hook - debugs and infos are passed through "debug," distinguishable by the "[debug] " prefix
        if re.search("^\[[a-z]+\]\s", msg):
            # info & debug msgs are sent thru error if -q and -v were passed, so we'll do the same here
            if self.debugsToError:
                self.wsHook.error(msg)
        else:
            self.wsHook.debug(msg)
    
    def info(self, msg):
        pass

    def warning(self, msg):
        self.wsHook.warning(msg)
    
    def error(self, msg):
        self.wsHook.error(msg)