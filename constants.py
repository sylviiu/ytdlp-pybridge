import sys
import json
import time
import os

os.makedirs('dist/build', exist_ok=True)
os.makedirs('dist-zip/build', exist_ok=True)

str = json.dumps({
    'Build number': os.environ['GITHUB_RUN_NUMBER'] if 'GITHUB_RUN_NUMBER' in os.environ else '-1',
    'Build arch': os.environ['RUNNER_ARCH'] if 'RUNNER_ARCH' in os.environ else 'unknown',
    'Python Version': sys.version.split(' ')[0],
    'Python Implementation': sys.implementation.name,
    'Commit': os.environ['GITHUB_SHA'] if 'GITHUB_SHA' in os.environ else 'unknown',
    'Built': int(time.time() * 1000),
}, ensure_ascii=False, default=lambda o: '<not serializable>')

open('dist/build/constants.json', 'w').write(str)
open('dist-zip/build/constants.json', 'w').write(str)