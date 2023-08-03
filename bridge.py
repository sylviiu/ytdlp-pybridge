import json
import threading
import actions
import sys
import yt_dlp
from c.out import out

import versionHeader

if len(sys.argv) == 2 and sys.argv[1] == "--version":
    versionHeader.printHeader(True)
    sys.exit(0)
elif len(sys.argv) == 2 and sys.argv[1] == "--version-json":
    versionHeader.printHeader(False)
    sys.exit(0)
elif len(sys.argv) > 1:
    yt_dlp.main()
else:
    versionHeader.printHeader()
    
    from c.print import print

    print("Creating bridge...")

    hooks = {}

    def recv(message):
        data = json.loads(message)

        if 'type' in data:
            print("Has type: " + data['type'])

            targetId = data['targetID'] if 'targetID' in data else data['id']

            print("ID: " + data['id'])
            print("Target ID: " + targetId)

            if(hasattr(actions, data['type'])):
                threading.Thread(target=getattr(actions, data['type'])(hooks[targetId] if targetId in hooks else targetId, data), name="ACTION THREAD / " + targetId, daemon=True).start()
            else:
                print("Unknown message type: " + data['type'])
        else:
            if data['id'] in hooks:
                hook = hooks[data['id']]
            else:            
                hook = actions.hook(data['id'], out)
                hooks[data['id']] = hook
            
            def complete():
                hooks[data['id']].complete()
                del hooks[data['id']]
                print("Completed task: " + data['id'])

            threading.Thread(target=actions.exec(hook, data, complete), name="ACTION THREAD / " + data['id'], daemon=True).start()

    def handleGlobalException(exc_type, exc_value, exc_traceback):
        print("Error in bridge (global exception): " + str(exc_type) + " - " + str(exc_value) + " - " + str(exc_traceback))

    sys.excepthook = handleGlobalException

    print("Bridge ready", flush=True)

    for line in sys.stdin:
        try:
            recv(line)
        except:
            exc_info = sys.exc_info()
            handleGlobalException(exc_info[0], exc_info[1], exc_info[2])