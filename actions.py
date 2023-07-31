import yt_dlp
import json
from c.writeStringWrapper import writeStringWrapper
from c.killableThread import killableThread
from c.cookiesBinding import cookiesBinding
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
        'resources': parsedOptions[2],
        'cookies': cookies
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

    print('parsed cookie', parsed['cookies'])

    write_string = writeStringWrapper(hook)

    killed = False

    def killDownload():
        nonlocal killed
        killed = True

    hook.setKill(killDownload)

    with yt_dlp.YoutubeDL(parsed['options']) as ytdl:
        print("cookiejar 1", ytdl.cookiejar)

        if parsed['cookies'] is not None:
            c = cookiesBinding(parsed['cookies'])

            print("cookiejar 1.25", c.cookies)

            ytdlCookieJar = yt_dlp.cookies.YoutubeDLCookieJar()
            ytdlCookieJar._really_load(c, filename=None, ignore_discard=False, ignore_expires=False)

            print("cookiejar 1.5", ytdlCookieJar)

            for cookie in ytdlCookieJar:
                # Treat `expires=0` cookies as session cookies
                if cookie.expires == 0:
                    cookie.expires = None
                    cookie.discard = True
            
            ytdl.cookiejar = ytdlCookieJar

        ytdl._write_string = write_string
        ytdl.write_string = write_string
        ytdl.write_debug = write_string

        def execDownload():
            print("cookiejar 1/2", ytdl.cookiejar)

            nonlocal killed
            if killed == True:
                print("cookiejar 2", ytdl.cookiejar)
                return complete()
            else:
                ytdl.download(parsed['resources'])
                print("cookiejar 3", ytdl.cookiejar)
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