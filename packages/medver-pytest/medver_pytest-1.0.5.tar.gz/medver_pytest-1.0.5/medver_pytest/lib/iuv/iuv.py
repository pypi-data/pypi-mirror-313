import os
import sys
import types

import pytest

from medver_pytest.lib import services
from medver_pytest.lib.iuv.iuv_data import IUVData
from medver_pytest.lib.iuv.iuv_requirements import IUVRequirements
from medver_pytest.lib.stdout_logger import StdoutLogger as logger


# -------------------
## Holds content for running an Intended Usa Verification Report
class IUV:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds reference to IUVRequirements object
        self._reqmts = None
        ## holds path to the IUV log file
        self._log_path = None
        ## holds reference to IUVData object
        self._data = None
        ## indicates if an abort() was called
        self._abort_called = False
        ## holds logger lines (if any)
        self._logger_lines = []
        ## holds logger lines (if any)
        self._stdout_lines = []

    # -------------------
    ## return the services object
    #
    # @return the services object
    @property
    def svc(self):
        return services

    # -------------------
    ## return the data object
    #
    # @return the data object
    @property
    def data(self):
        return self._data

    # -------------------
    ## return whether or not abort() was called
    #
    # @return the abort flag
    @property
    def abort_called(self):
        return self._abort_called

    # -------------------
    ## return current list of logger lines
    #
    # @return the logger lines
    @property
    def logger_lines(self):
        return self._logger_lines

    # -------------------
    ## return current list of stdout lines
    #
    # @return the stdout lines
    @property
    def stdout_lines(self):
        return self._stdout_lines

    # -------------------
    ## simulate a print to stdout
    #
    # @param line  the line to save
    # @return None
    def print(self, line):  # print okay
        self._stdout_lines.append(line)

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        self._reqmts = IUVRequirements()
        self._reqmts.init()

        self._log_path = os.path.join('out', 'iuv.log')
        self._write('=====')

        self._data = IUVData()
        self._data.init()

        self.init2()

    # -------------------
    ## initialization - stage2
    #
    # @return None
    def init2(self):
        self._abort_called = False
        self._logger_lines = []
        self._stdout_lines = []

    # -------------------
    ## initialize after each test
    #
    # @return None
    def init_each_test(self):
        logger.line('')
        self._stdout_lines = []

    # -------------------
    ## save a logger line
    #
    # @param line   the line that was logged
    # @return None
    def mock_logger(self, line):
        self._logger_lines.append(line)

    # -------------------
    ## clear current logger content
    #
    # @return None
    def clear_logger(self):
        self._logger_lines = []

    # -------------------
    ## indicate abort was called
    #
    # @param msg   optional message to print
    # @return None
    def abort(self, msg=None):
        self._abort_called = True
        logger.line('IUV: iuv.abort() called')
        logger.line(f'IUV: iuv.abort() msg: {msg}')
        logger.line('IUV: exiting testcase (ignore next "SKIPPED")')
        pytest.skip('IUV abort')

    # -------------------
    ## IUV verify - called to verify a value for a particular reqid or set of reqids
    # The requirements are for the IUV report.
    #
    # @param expected   the expected value
    # @param actual     the actual value
    # @param reqids     list of
    # @return None
    def iuv_verify(self, expected, actual, reqids):
        if not services.cfg.iuvmode:
            services.abort('IUV: iuv.iuv_verify() can only be used in --iuvmode')

        tb, location = self._get_location()

        if isinstance(reqids, str):
            reqids = [reqids]
        elif isinstance(reqids, list):
            pass
        else:
            services.logger.err(f'IUV: reqids should be a str or list, found: {type(reqids).__name__}')
            return

        s = []
        for reqid in reqids:
            s.append(reqid.upper())
        reqids = s

        # check reqid was specified
        self._check_reqids(reqids, location)

        expected_type = type(expected).__name__
        actual_type = type(actual).__name__

        # write the info to the IUV log
        if expected == actual:
            res = 'PASS'
            passed = True
        else:
            res = 'FAIL'
            passed = False

        msg = self._write_result(res, location, reqids, expected_type, expected, actual_type, actual)

        # save the reqid to the trace file
        self._reqmts.save_reqids_to_trace(reqids, passed, location)

        if not passed:
            raise AssertionError(msg).with_traceback(tb)

    # -------------------
    ## get the location of the calling iuv_verify() function
    #
    # @return None
    def _get_location(self):
        tb = None
        try:
            raise AssertionError
        except AssertionError:
            tb = sys.exc_info()[2]

        # go two caller back
        frame = tb.tb_frame
        frame = frame.f_back
        frame = frame.f_back

        tb = types.TracebackType(tb_next=None,
                                 tb_frame=frame,
                                 tb_lasti=frame.f_lasti,
                                 tb_lineno=frame.f_lineno)

        location = f'{tb.tb_frame.f_code.co_filename}({tb.tb_frame.f_lineno})'
        return tb, location

    # -------------------
    ## check the reqmt ids passed in are valid and recognized values for the IUV SRS
    #
    # @param reqids    the reqid list for this call
    # @param location  the iuv_verify() location
    # @return None
    def _check_reqids(self, reqids, location):
        for reqid in reqids:
            msg = self._reqmts.check(reqid, location)
            if msg is not None:
                services.abort(msg)

    # -------------------
    ## write the result of the iuv_verify call to the log and to the trace json file
    #
    # @param result          either PASS or FAIL
    # @param location        the iuv_verify() location
    # @param reqids          the reqid list for this call
    # @param expected_type   the type of the expected value
    # @param expected        the expected value
    # @param actual_type     the type of the actual value
    # @param actual          the actual value
    # @return the formatted message line
    def _write_result(self, result, location, reqids, expected_type, expected, actual_type, actual):
        msg = f'{result} verify: {location}\n' \
              f'     Expected: ({expected_type: <5}): {expected}\n' \
              f'     Actual  : ({actual_type: <5}): {actual}'
        self._write(msg)

        # get the requirement desc
        for reqid in reqids:
            desc = self._reqmts.get(reqid)
            self._write(f'     Reqid   : "{reqid}" {desc}')

        self._write('')
        return msg

    # -------------------
    ## write the given line to the log; write the trace json file to disk
    #
    # @param line  the line to write to the IUV log
    # @return None
    def _write(self, line):
        with open(self._log_path, 'a', encoding='utf-8') as log:
            log.write(f'{line}\n')

        self._reqmts.save_trace()

    # -------------------
    ## print report summary of IUV PASS/FAIL to stdout
    #
    # @return None
    def report(self):
        logger.line('')

        ## see function self._log
        self._reqmts.report_trace(self._log)
        self._reqmts.report_missing(self._log)

    # --------------------
    ## print a line to stdout
    #
    # @param tag    a tag for logging
    # @param val    the value to write
    # @param total  optional total value used to calculate a percentage
    # @return None
    def _log(self, tag, val=None, total=None):
        if tag == '':
            logger.line('')
            return

        if val is None:
            logger.line(tag)
        elif total is None:
            logger.line(f'   {tag: <25} {val: >5}')
        elif total == 0:
            logger.line(f'   {tag: <25} {val: >5} (total is 0)')
        else:
            logger.line(f'   {tag: <25} {val: >5} {round(val / total * 100.0, 0):>5}%')
