<h1 align="center">
  <img src="https://raw.githubusercontent.com/sylviiu/ezytdl/main/res/img/heading.png" height="128px"/><br>
</h1>

A simple python bridge utilizing yt-dlp's Python API that ezytdl depends on.

This eliminates the need of launching multiple yt-dlp processes for different requests, and uses a single python process that uses its own threading.

*(this is best used with another program that wants to use "closest to native" yt-dlp)*

-------------------------

## Outputs

`stderr` and `stdout` are used for different purposes.

`stderr` is used for the program's "debug logs" (which has nothing to do with the actual yt-dlp output for the program); `stdout` is used for the actual yt-dlp output.

Each output in stdout is split by `\r\n` (i know it's backwards but `\n\r` didn't have an effect for me for some reason), and often will be split into chunks without finishing with the aforementioned characters. A way I worked around this (in ezytdl) would be as follows:

```js
let existingData = ``;

module.exports.bridgeProc.stdout.on(`data`, data => {
    if(!data.toString().includes(`\n\r`)) {
        existingData += data.toString();
        return;
    } else {
        if(existingData) {
            data = existingData + data.toString();
            existingData = ``;
        }

        const parse = (msg) => {
            const data = JSON.parse(msg.toString().trim());
            if(data.id) {
                module.exports.idHooks.filter(h => h.id == data.id).forEach(h => h.func(data));
            } else if(!module.exports.bridgeVersions) {
                module.exports.bridgeVersions = data;
            }
        }

        data.toString().trim().split(`\n\r`).forEach((msg, i) => {
            try {
                parse(msg)
            } catch(e) {
                try {
                    parse(`{` + msg.toString().trim().split(`{`).slice(1).join(`{`).split(`}`).slice(0, -1).join(`}`) + `}`)
                } catch(e) {
                    existingData += msg.toString();
                }
            }
        })
    }
});
```

...basically, if the data doesn't include `\n\r`, it will be added to a variable, and if it does, it will be split by `\n\r` and parsed as JSON. If it fails to parse as JSON, it will try to parse it as JSON again, but trimmed to the first `{` and last `}`. If it fails again, it will be added to the variable.

*for some reason this works. i don't understand it anymore, but it works.*

-------------------------

## Usage

Everything is handled through `stdin`. Just input a JSON string with the following format:

```jsonc
{
    "id": "unique id (can be auto-generated -- this is how you can identify the output of a request)",
    "args": ["--args", "for", "yt-dlp"]
}
```

...and when a request starts a task, it will give you the following output:

```jsonc
{
    "id": "unique id (as previously added)",
    "type": "info | warning | error | infodump", // info = yt-dlp's stdout, warning & error = yt-dlp's stderr, infodump = yt-dlp's dumped info json on every request it provides one
    "content": "(the output of the log -- this should be the same as the output of yt-dlp's stdout)"
}
```

...and when a task completes, it will give you the following output:

```jsonc
{
    "id": "unique id (as previously added)",
    "type": "complete",
    "content": 0 // exit code, 0 = success, 1 = error, can be null
}
```

If you want to kill a process, you can input the following:

```jsonc
{
    "id": "unique id (as previously added)",
    "type": "kill"
}
```

...and it should return the same output as if it completed.