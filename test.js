const child_process = require('child_process');

const path = process.argv[2];

console.log(`Starting bridge at ${path}`);

const proc = child_process.execFile(path, {
    env: Object.assign({}, process.env, {
        PYTHONUNBUFFERED: 1,
    })
});

proc.on('error', (err) => {
    console.log(`Bridge failed to start: ${err}`);
    process.exit(1)
});

proc.once('exit', (code) => {
    console.log(`Bridge exited with code ${code}`);
    process.exit(code)
})

let allData = ``;

const handleData = (data) => {
    allData += data.toString();

    console.log(data.toString());

    if(allData.includes(`Bridge ready`)) {
        console.log(`Bridge has successfully started.`);
        process.exit(0)
    }
}

proc.stderr.on('data', handleData);
proc.stdout.on('data', handleData);

setTimeout(() => {
    console.log(`Bridge did not start in time.`);
    process.exit(1)
}, 15000)