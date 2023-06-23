import json
from c.print import print

def printHeader():
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

    print(json.dumps(versionObj, ensure_ascii=False, default=lambda o: '<not serializable>'), flush=True)