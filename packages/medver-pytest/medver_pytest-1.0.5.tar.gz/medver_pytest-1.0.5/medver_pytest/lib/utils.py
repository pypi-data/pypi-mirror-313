import datetime
import os
import sys

from . import services


# -------------------
## holds various utility functions
class Utils:

    # -------------------
    ## gets the location of the caller
    #
    # @param levels   default 3; used to go back further in the trace back
    # @return a string showing the filename and line number of the caller
    @staticmethod
    def get_location(levels=3):
        # get a full stackframe
        tb = None
        try:
            raise AssertionError
        except AssertionError:
            tb = sys.exc_info()[2]

        # go levels callers back
        frame = tb.tb_frame
        while levels > 0:
            frame = frame.f_back
            levels -= 1

        # uncomment to debug
        # logger.line('')
        # logger.dbg(frame.f_code.co_name)
        # logger.dbg(frame.f_code.co_filename)
        # logger.dbg(frame.f_lineno)

        fname = os.path.basename(frame.f_code.co_filename)
        location = f'{fname}({frame.f_lineno})'
        return location

    # -------------------
    ## gets the current time in utc or local time
    #
    # @param use_cfg_fmt  if True, use the format given in cfg.json, otherwise use short ofrm
    # @param use_time     if None, use the current UTC, otherwise use the given time
    # @return a string showing the current date_time with
    @staticmethod
    def get_dts(use_cfg_fmt, use_time=None):
        # assume use_time is UTC
        if use_time is not None:
            dts = use_time
        else:
            dts = Utils.get_utc()

        if not services.cfg.use_utc:
            dts = dts.astimezone()

        if use_cfg_fmt:
            dts = dts.strftime(services.cfg.dts_format)
        else:
            dts = dts.strftime('%Y-%m-%d %H:%M:%S')
        return dts

    # -------------------
    ## gets the current UTC time as a datetime
    #
    # @return a datetime object with UTC time in it
    @staticmethod
    def get_utc():
        return datetime.datetime.now(datetime.timezone.utc)
