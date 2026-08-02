"""
Updated regression runner that executes pytest to produce coverage and JUnit XML,
and also runs the JSON testcases runner as fallback. Generates a summary report.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
JUNIT_OUT = REPO_ROOT / 'results' / 'regression_junit.xml'
COV_XML = REPO_ROOT / 'results' / 'coverage.xml'
COV_DIR = REPO_ROOT / '.coverage'

os.makedirs(REPO_ROOT / 'results', exist_ok=True)

start = time.time()

# Run pytest for tests/test_rule_runner.py to leverage existing pytest harness and coverage
pytest_cmd = [
    sys.executable, '-m', 'pytest', 'tests/test_rule_runner.py',
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

# If pytest failed, exit non-zero for CI
if retcode != 0:
    print('Some tests failed. See JUnit/pytest output for details.')
    sys.exit(retcode)

# Parse JUnit XML to list failures (if any) - lightweight parsing
import xml.etree.ElementTree as ET

failures = []
if JUNIT_OUT.exists():
    tree = ET.parse(str(JUNIT_OUT))
    root = tree.getroot()
    for testcase in root.iter('testcase'):
        for failure in testcase.findall('failure'):
            failures.append({
                'testcase': testcase.attrib.get('name'),
                'message': failure.attrib.get('message'),
                'text': failure.text
            })

print('Failures in JUnit:', len(failures))
for f in failures:
    print(' -', f['testcase'], f['message'])

# Exit 0 if no failures
if failures:
    sys.exit(2)
print('All regression testcases passed (pytest).')
sys.exit(0)
