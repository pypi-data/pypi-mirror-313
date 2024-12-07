* website: <https://arrizza.com/medver-pytest>
* installation: see <https://arrizza.com/setup-common>

## Summary

medver-pytest is a python module that provides verification functions
for generating an FDA compliant set of reports. The generation of the raw test data
can be done with Python scripts or by manual or semi-automated scripts.

* it uses pytest to invoke the scripts, all of pytest functionality is available
* set of automated test functions
* set of Manual test functions
* 4 reports:
    * Test Protocol
    * Test Report
    * Trace Matrix
    * Summary

The verification test cases are written in Python which uses
the pytest module to invoke the test cases. During
execution, various data is captured. The data is then used by
the report facility to generate Test Protocol, Test Report
and Trace Matrix documents in docx, pdf and text formats. A
summary is also generated indicating percentage of requirements
that are complete, passing/failing etc.

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat.cfg](https://arrizza.com/user-guide-xplat.cfg) to configure xplat.cfg file.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Tutorial

A tutorial with sample verification scripts for a (simulated!) IV pump is
here <https://arrizza.com/medver-pytest-tutorial>.
There is a User Guide with full details there.

The tutorial repo is used to help develop medver-pytest and
to ensure it's provides a comprehensive set of functions.

That repo tests a simulated IV pump
application, including a set of requirements and test scripts
that use medver-pytest. A sample set of reports can be generated
and reviewed.

There are also a few other repos that have used medver-pytest, again for proof-of-concept
and comprehensive set of useful functions:

* <https://bitbucket.org/arrizza-public/socket-oneline/src/master/>
* <https://bitbucket.org/arrizza-public/gui-api-tkinter/src/master/>

## Usage

```bash
pip install medver-pytest
```

* See the tutorial repo <https://bitbucket.org/arrizza-public/medver-pytest-tutorial/src/master/>
  for full instructions on how to use medver-pytest

* See User Guide.docx in the medver-pytest-tutorial repo for additional details

### Quick Guide

* the file test_sample.py shows various examples of using medver-pytest.
* to invoke all tests use:

```bash
./doit
```

or invoke a subset of test cases:

```bash
# the "-k" switch is part of pytest
./doit -k test_0

# invoke only passing tests that are fully automated
./doit -k "not semi and not fails"

# invoke only semi-manual tests
./doit -k "semi"
```

### invoking the test_sample script

The test is run in doit by:

```bash
function run_it()
```

The report is run in doit by:

```bash
function run_report()
```

see out/ver directory for pdf or docx reports

## Installation

The doc/installation_*.md files contain additional information
for installing medver-pytest
for various supported platforms:

* installation_macos.md : MAC OS
* installation_msys2.md : MSYS2 on Windows
* installation_ubu.md   : Ubuntu

## Python environment

Note that the set_env.sh script sets the python environment for
various platforms and sets variables

* $pyexe - the python executable
* $pybin - the location of the environment bin directory

```bash
source set_env.sh
source "${pybin}/activate"
# ... skip ...
$pyexe helpers/ver_report.py
````

## Report Output

* the output files are in the out/ver directory

```bash
ls out/ver
medver_pytest.log # the log output
medver_pytest.txt # output from doit script
*_protocol.json   # data generated during the test case run
summary.docx      # docx version of summary document
summary.pdf       # pdf version of summary document
summary.txt       # text version of summary document
test_protocol.*   # test protocol document in various formats
test_report.*     # test report document in various formats
trace.*           # trace matrix document in various formats 
```

## Check conftest.py

If you want to use the medver-pytest command line switches from pytest,
ensure you call the cli_addoption() and cli_configure() functions in conftest.py

```python
from medver_pytest import pth


# -------------------
def pytest_addoption(parser):
    pth.cfg.cli_addoption(parser)


# -------------------
def pytest_configure(config):
    pth.cfg.cli_configure(config)
```

## Writing a test case

* import unittest and pytest as normal. Then import medver_pytest:

```python
import unittest
import pytest
from medver_pytest import pth
```

Note: 'pth' is a global that holds a reference to PytestHarness.
The harness holds references to all classes needed during a test run.

* next create a normal unit test for pytest/unittest

```python
# -------------------
class TestSample(unittest.TestCase):
  # --------------------
  @classmethod
  def setUpClass(cls):
    pth.init()

  # -------------------
  def setUp(self):
    pass

  # -------------------
  def tearDown(self):
    pass

  # --------------------
  @classmethod
  def tearDownClass(self):
    pth.term()
```

* To create a protocol use pth.proto.protocol() with a protocol
  id and description
* To create steps within that protocol, use pth.proto.step()

```python
# --------------------
def test_0(self):
    # declare a new protocol id and it's description
    pth.proto.protocol('tp-000', 'basic pass/fail tests')
    pth.proto.set_dut_serialno('sn-0123')

    pth.proto.step('try checks with 1 failure')
    pth.ver.verify_equal(1, 2, reqids='SRS-001')
    pth.ver.verify_equal(1, 1, reqids='SRS-002')
    pth.ver.verify_equal(1, 1, reqids='SRS-003')
    pth.proto.comment('should be 1 failure and 2 passes')
```

at this point, there is one protocol TP-000 that has 1 step.

Use doit to run it:

```bash
./doit -k test_0
```

### Output

Check the stdout or the out/ver/medver_pytest.txt file:

* indicates that a failure occurred
* the return code from the script is non-zero

### Report documents

Check the generated documents in the out/ver/ directory.

* summary.pdf should indicate:
    * there are a total of 7 requirements (see srs_sample.json)
    * there are 2 passing requirements which is 28.8% of all
      requirements
    * there is 1 failing requirement which is 14.3% of all
      requirements
    * there are 4 requirements that were not tested which is
      57.1% of all requirements

* test_report.pdf and/or test_protocol.pdf should indicate:
* the test run type is "dev" so this was not a formal run
* the test run id is "dev-001". This can be set in cfg.json to
  track individual test runs
* the date time the document was generated

* There should be one protocol TP-000
* The location of the protocol is test_sample.py(line number)
* The protocol had only 1 step which tested requirement SRS-001
* The report document shows the expected and actual values and
  that result was a FAIL,
  and the location of the failing verify() function
* The report document shows a comment
* There is table after the protocol showing the requirement
  SRS-001 and it's description
* Note the header and footer information comes from the cfg.json
  file

### Pytest markers

* you can use pytest markers as normal

```python
# --------------------
# @pytest.mark.skip(reason='skip')
@pytest.mark.smoketest1
def test_init2(self):
    pth.proto.protocol('tp-002', 'test the init2')

    pth.proto.step('verify1 everything is equal')
    pth.ver.verify(1 == 1, reqid='SRS-001')
    # note: this is the second time this requirement is verified


# --------------------
# @pytest.mark.skip(reason='skip')
def test_init3(self):
    pth.proto.protocol('tp-003', 'test the init3')

    pth.proto.step('verify1 everything is equal')
    pth.ver.verify(1 == 1, reqid='SRS-004')
```

## Verification Functions

* To create verification tests use pth.ver.verify()

```python
# note: you can use normal pytest and unittest functions
# but their results won't show up in the report
self.assertEqual(x, y)

# do a verification against a requirement
pth.ver.verify_equal(x, y, reqid='SRS-001')
pth.ver.verify_equal(x, 1, reqid='SRS-001')
# since all verifys passed, this step's result is PASS

pth.proto.step('verify2')
pth.ver.verify(False, reqid='SRS-002')
pth.ver.verify(True, reqid='SRS-002')
pth.ver.verify(True, reqid='SRS-002')
# since one verify failed, this step's result is FAIL

pth.proto.step('verify3')
pth.ver.verify(True, reqid='SRS-003')
pth.ver.verify(True, reqid='SRS-003')
pth.ver.verify(False, reqid='SRS-003')
# since one verify failed, this step's result is FAIL
```

* See doc/User Guide.docx for a full list of verification functions

```python
verify(actual)  # verify actual is true
verify_true(actual)  # verify actual is true
verify_false(actual)  # verify actual is false
verify_equal(expected, actual)  # verify actual == expected
verify_not_equal(expected, actual)  # verify actual != expected
verify_none(actual)  # verify actual is None
verify_is_none(actual)  # verify actual is None
verify_not_none(actual)  # verify actual is not None
verify_in(actual, exp_list)  # verify actual is in the expected list
verify_not_in(actual, exp_list)  # verify actual is not in the expected list
verify_lt(left, right)  # verify left < right
verify_le(left, right)  # verify left <= right
verify_gt(left, right)  # verify left > right
verify_ge(left, right)  # verify left >= right
verify_reqex(actual, regex)  # verify actual matches the regex
verify_not_reqex(actual, regex)  # verify actual does not match the regex
verify_delta(expected, actual, abs_tolerance)  # verify actual == expected within +/- tolerance
verify_not_delta(expected, actual, abs_tolerance)  # verify actual outside +/- tolerance
verify_delta_pct(expected, actual, pct_tolerance)  # verify actual == expected within +/- percent
verify_not_delta_pct(expected, actual, pct_tolerance)  # verify actual outside +/- percent
```

* A pass does not generate any stdout
* A fail reports various information
    * the location of the failure
    * the expected value (and it's python type)
    * the actual value (and it's python type)
    * a traceback at the time of the failures

```bash
FAILURE: at test_sample.py(37)
   Expected (int)     : 1
   Actual   (int)     : 2
test_sample.py:37 in test_0() -> pth.ver.verify_equal(1, 2, reqids='SRS-001')
medver_pytest/lib/verifier.py:98 in verify_equal() -> self._handle_fail(rs)
medver_pytest/lib/verifier.py:412 in _handle_fail() -> raise AssertionError(f'at {rs.location}{msg}')
```

* The test_report.txt document shows some additional information:
    * the protocol id and description and its location
    * which step failed
    * the date time stamp (dts) when the failure occurred
    * the requirement id

```bash
==== protocol: TP-000 basic pass/fail tests
     location: test_sample.py(33)
     Step 1  : try checks with 1 failure
       > dts          : 2022-12-11 06:00:52
       > result       : FAIL
       > actual       : 2
       > actual raw   : 2
       > expected     : 1
       > expected raw : 1
       > reqids       : {'SRS-001': 1}
       > location     : test_sample.py(37)
```

## Generate Report

* to generate a report use: pth.report()

* see helpers/ver_report.py

```python
import os
import sys

sys.path.insert(1, os.path.join('.'))

from medver_pytest import *  # noqa

# generate the report
pth.cfg.cli_parse()
# force iuvmode to be
pth.cfg.cli_set('iuvmode', False)

pth.init(report_mode=True)
pth.report()
pth.term()
```

to invoke it:

```bash
$pyexe helpers/ver_report.py
```
