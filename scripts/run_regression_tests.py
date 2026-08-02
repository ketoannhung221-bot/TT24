"""
Updated regression runner to run full test suite, produce JUnit and coverage outputs, and generate summary including execution time.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / 'results'
JUNIT_OUT = RESULTS_DIR / 'regression_junit.xml'
COV_XML = RESULTS_DIR / 'coverage.xml'

os.makedirs(RESULTS_DIR, exist_ok=True)

start = time.time()

# Run pytest for the entire tests/ directory to produce JUnit XML and coverage
pytest_cmd = [
    sys.executable, '-m', 'pytest', 'tests',
    '--junitxml', str(JUNIT_OUT),
    '--cov=services', '--cov-report=xml:' + str(COV_XML), '-q'
]
print('Running:', ' '.join(pytest_cmd))
res = subprocess.run(pytest_cmd, cwd=str(REPO_ROOT))
retcode = res.returncode

end = time.time()
elapsed = end - start

# Summarize
print('\nREGRESSION SUMMARY')
print('Elapsed time: %.2fs' % elapsed)
print('Pytest return code:', retcode)
print('JUnit report:', JUNIT_OUT)
print('Coverage XML:', COV_XML)

# Parse JUnit XML to list failures
import xml.etree.ElementTree as ET

failures = []
if JUNIT_OUT.exists():
    tree = ET.parse(str(JUNIT_OUT))
    root = tree.getroot()
    for testcase in root.iter('testcase'):
        for failure in testcase.findall('failure'):
            failures.append({
                'testcase': testcase.attrib.get('classname') + '.' + testcase.attrib.get('name') if testcase.attrib.get('classname') else testcase.attrib.get('name'),
                'message': failure.attrib.get('message'),
                'text': (failure.text or '').strip()
            })

print('Failures in JUnit:', len(failures))
for f in failures:
    print(' -', f['testcase'], f['message'])

# Exit 0 if no failures
if failures:
    sys.exit(2)
print('All regression tests passed.')
sys.exit(0)
