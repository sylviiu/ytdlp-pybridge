import re
from .print import print

class Logger:
    def __init__(self, wsHook, debugsToError=False):
        self.wsHook = wsHook
        self.debugsToError = debugsToError
    
    def debug(self, msg):
        # https://github.com/yt-dlp/yt-dlp#adding-logger-and-progress-hook - debugs and infos are passed through "debug," distinguishable by the "[debug] " prefix
        if re.search("^\[[a-z]+\]\s", msg):
            # pybridge previously sent info & debug msgs thru error (presumably yt-dlp's default logger), so we'll do the same here
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