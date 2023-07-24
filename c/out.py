import sys
import io

enc = 'utf-8'

#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding=enc, buffering=1)
new_stdout = io.TextIOWrapper(sys.stdout.detach(), encoding=enc)
sys.stdout = new_stdout

#sys.stderr = open(sys.stderr.fileno(), mode='w', encoding=enc, buffering=1)
new_stderr = io.TextIOWrapper(sys.stderr.detach(), encoding=enc)
sys.stderr = new_stderr

def out(data):
    if hasattr(data, 'decode'):
        data = data.decode(enc, 'replace')
    
    if(type(data) != 'str'):
        data = str(data)
    
    data = data.encode(enc, 'replace').decode(enc, 'replace')
    
    sys.stdout.write(data + '\n\r')
    #sys.stdout.write((data.encode('utf-8', 'replace') if hasattr(data, 'encode') else data + '\n\r').decode('utf-8', 'replace'))
    sys.stdout.flush()