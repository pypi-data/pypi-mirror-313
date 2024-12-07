import os

from .. import services
from ..utils import Utils


# -------------------
## Holds all info for the logger file
class Logger:
    # -------------------
    ## constructor
    def __init__(self):
        ## the logger file pointer
        self._fp = None
        ## the current line count of the log file; used to determine when to flush
        self._line_count = 0
        ## the current DTS count; used to determine when to write the DTS to the log
        self._dts_count = 0
        ## the last DTS; used to show the elapsed time
        self._dts_last = None

    # -------------------
    ## intialize
    #
    # @param fname   the file name to write to; default medver_pytest.log
    # @return None
    def init(self, fname='medver_pytest.log'):
        path = os.path.join(services.cfg.outdir, fname)
        self._fp = open(path, 'w')

    # -------------------
    ## write a "start" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def start(self, msg):
        self._write_line('====', msg, so=False)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def line(self, msg):
        self._write_line(' ', msg, so=False)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def ok(self, msg):
        self._write_line('OK', msg, so=True)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def warn(self, msg):
        self._write_line('WARN', msg, so=True)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def err(self, msg):
        self._write_line('ERR', msg, so=True)

    # -------------------
    ## write a "raw" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def raw(self, msg):
        self._write_line('', msg, so=True, raw=True)

    # -------------------
    ## write a "user" line with the given message
    # this indicates an action taken by a tester e.g. clicking, ctrl-c
    #
    # @param msg   the message to write
    # @return None
    def user(self, msg):
        self._write_line('USER', msg, so=False, raw=False)

    # -------------------
    ## write the given line to the log. Optionally write it stdout
    #
    # @param tag   the prefix tag
    # @param msg   the message to write
    # @param so    if True, write to stdout
    # @param raw   if True, write the line without the tag or timestemp
    # @return None
    def _write_line(self, tag, msg, so=False, raw=False):
        if self._dts_count == 0:
            # capture the current dts in UTC and save it for doing the delta per line
            self._dts_last = Utils.get_utc()
            dts = Utils.get_dts(use_cfg_fmt=True, use_time=self._dts_last)

            line = f'{"----": <4} {dts}'
            self._fp.write(f'{line}\n')

            # print full dts every so often
            self._dts_count = 100

        if raw:
            line = msg
            self._fp.write(msg)
        else:
            line = f'{tag: <4} {msg}'

            self._dts_count -= 1

            # add time delta to log lines; self_dts.last is always UTC
            diff = Utils.get_utc() - self._dts_last
            self._fp.write(f'{diff} {line}\n')

        # ok to flush?
        self._line_count += 1
        if self._line_count > 5:
            self._fp.flush()

        # ok to write to stdout?
        if services.cfg.iuvmode:  # pragma: no cover
            # coverage: iuvmode is only set during IUV and UT runs
            services.harness.iuv.mock_logger(line)
        elif so:  # pragma: no cover
            # coverage: not used during IUV and UT runs
            print(line)  # print okay
