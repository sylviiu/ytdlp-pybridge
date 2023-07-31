import sys
import builtins

def print(*msgs, flush=True):
    for msg in msgs:
        sys.stderr.write(str(msg) + "\n\r")
        sys.stderr.flush()
        #builtins.print(msg, file=sys.stderr, flush=flush)