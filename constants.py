import sys
import json
import time
import os
import subprocess

os.makedirs('dist/build', exist_ok=True)

str = json.dumps({
    'Build number': os.environ['GITHUB_RUN_NUMBER'] if 'GITHUB_RUN_NUMBER' in os.environ else '-1',
    'Build arch': os.environ['RUNNER_ARCH'] if 'RUNNER_ARCH' in os.environ else 'unknown',
    'Python': sys.version.split(' ')[0],
    'Built': int(time.time() * 1000),
    'Supported sites': json.loads(subprocess.check_output(['node', os.path.join('devscripts', 'generateSupportedSites.js')]).decode('utf-8'))
}, ensure_ascii=False, default=lambda o: '<not serializable>')

open('dist/build/constants.json', 'w').write(str)