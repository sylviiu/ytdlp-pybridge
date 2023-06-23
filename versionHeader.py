import json
import sys
import os
from c.print import print

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

def printHeader(string=False):
    import yt_dlp
    import sys

    versionObj = {
        'ezytdl-pybridge': {
            'Python Version': sys.version.split(' ')[0],
            'Python Implementation': sys.implementation.name,
        },
        'yt-dlp': {
            'Channel': yt_dlp.version.CHANNEL,
            'Version': yt_dlp.version.__version__,
            'Commit': yt_dlp.version.RELEASE_GIT_HEAD
        }
    }

    if os.path.exists(os.path.join(bundle_dir, 'constants.json')):
        versionObj['ezytdl-pybridge'] = json.loads(open(os.path.join(bundle_dir, 'constants.json'), 'r').read())

    if string:
        for key in versionObj.keys():
            print("" + key + ":")
            for subkey in versionObj[key].keys():
                print("    " + subkey + ": " + str(versionObj[key][subkey]))
    else:
        print(json.dumps(versionObj, ensure_ascii=False, default=lambda o: '<not serializable>'), flush=True)