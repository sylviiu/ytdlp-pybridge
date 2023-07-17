import yt_dlp
import json
from c.writeStringWrapper import writeStringWrapper
from c.killableThread import killableThread
from c.print import print
from c.out import out

import c.wsHook as wsHook
from c.progressHook import progressHook

extractors = yt_dlp.extractor.gen_extractors()

def parseOptions(opt, hook):
    parsedOptions = yt_dlp.parse_options(opt)

    returnOptions = {
        'options': parsedOptions[3],
        'resources': parsedOptions[2]
    }

    returnOptions['options']['progress_hooks'] = [ progressHook(hook) ]
    returnOptions['options']['progress_with_newline'] = True
    #returnOptions['options']['no_color'] = True

    return returnOptions

def hook(id, func):
    print("Creating hook for id: " + id)
    return wsHook.hook(id, func)

def isvalidurl(id, data):
    thisHook = hook(id, out)

    def fallback():
        thisHook.debug(json.dumps({
            'extractor': None,
            'url': data['url'],
            'valid': False
        }))
        thisHook.complete()

    if 'url' in data:
        for extractor in extractors:
            if extractor.suitable(data['url']):
                thisHook.debug(json.dumps({
                    'extractor': extractor.IE_NAME,
                    'url': data['url'],
                    'valid': True
                }))
                
                return thisHook.complete()
                
        return fallback()
    else:
        return fallback()

def kill(hook, data):
    if(hook is not None and hasattr(hook, 'kill')):
        hook.kill()
        del hook
    else:
        print("No hook (or kill function) found for id: " + data['id'])

def exec(hook, data, complete):
    parsed = parseOptions(data['args'], hook)

    write_string = writeStringWrapper(hook)

    killed = False

    def killDownload():
        nonlocal killed
        killed = True

    hook.setKill(killDownload)

    with yt_dlp.YoutubeDL(parsed['options']) as ytdl:
        ytdl._write_string = write_string
        ytdl.write_string = write_string
        ytdl.write_debug = write_string

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