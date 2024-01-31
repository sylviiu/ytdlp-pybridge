import yt_dlp
import json
from io import StringIO
from c.killableThread import killableThread
from c.logger import Logger
from c.print import print
from c.out import out

import c.wsHook as wsHook
from c.progressHook import progressHook

extractors = yt_dlp.extractor.gen_extractors()

def parseOptions(opt, hook):
    cookies = None

    if '--cookiestxt' in opt:
        cookiesIndex = opt.index('--cookiestxt')
        cookies = opt[cookiesIndex + 1]
        del opt[cookiesIndex]
        del opt[cookiesIndex]

    parsedOptions = yt_dlp.parse_options(opt)

    returnOptions = {
        'options': parsedOptions[3],
        'resources': parsedOptions[2]
    }

    if cookies is not None:
        print("Using cookies with StringIO")
        returnOptions['options']['cookiefile'] = StringIO(cookies)

    returnOptions['options']['progress_hooks'] = [ progressHook(hook) ]
    returnOptions['options']['progress_with_newline'] = True
    returnOptions['options']['logger'] = Logger(hook, (opt.__contains__('--verbose') or opt.__contains__('-v')))
    #returnOptions['options']['no_color'] = True

    return returnOptions

def hook(id, func):
    print("Creating hook for id: " + id)
    return wsHook.hook(id, func)

def isvalidurl(id, data):
    thisHook = hook(id, out)

    available = []

    if 'url' in data and type(data['url']) == str:
        for extractor in extractors:
            if extractor.IE_NAME != 'generic' and extractor.suitable(data['url']) and extractor.IE_NAME not in available:
                available.append(extractor.IE_NAME)
                
    thisHook.debug(json.dumps({
        'extractors': available,
        'url': data['url'],
        'valid': True if len(available) > 0 else False
    }))

    return thisHook.complete()

def kill(hook, data):
    if(hook is not None and hasattr(hook, 'kill')):
        hook.kill()
        del hook
    else:
        print("No hook (or kill function) found for id: " + data['id'])

def exec(hook, data, complete):
    parsed = parseOptions(data['args'], hook)

    killed = False

    def killDownload():
        nonlocal killed
        killed = True

    hook.setKill(killDownload)

    with yt_dlp.YoutubeDL(parsed['options']) as ytdl:
        def execDownload():
            nonlocal killed
            if killed == True:
                return complete()
            else:
                ytdl.download(parsed['resources'])
                complete()

        t = killableThread(target=execDownload, name="YTDL THREAD", daemon=True)

        t.setHook(hook)

        def killDownload():
            nonlocal killed
            killed = True
            if t.is_alive():
                t.raiseExc(SystemExit)

        hook.setKill(killDownload)

        t.start()