# TODO rename for compatibility with MVC
# TODO move cfg, status, storage to model.cfg, etc

## holds configuration information
cfg = None

## holds information that spans multiple runs
status = None

## holds stored information about all test runs
storage = None

# TODO move proto, trace, summary to ctrl.proto, etc.

## holds protocol information about the current test run
proto = None

## holds trace matrix information about the current test run
trace = None

## holds summary information about the current test run
summary = None

## holds logger
logger = None

## holds test harness object
harness = None

## holds IUV object for use during self-testing
iuv = None

## holds the main window used for manual steps and verification
view = None


# -------------------
def abort(msg=None):
    # may be called by IUV, by UT, by User, or by normal operations
    if msg is None:
        line = 'abort called'
    else:
        line = f'abort called: {msg}'

    # logger may or may not be defined
    if logger is None:
        # print okay
        print(line)  # pragma: no cover
        # coverage: logger is always defined in IUV
    else:
        logger.err(line)

    import pytest

    if cfg.iuvmode:  # pragma: no cover
        # coverage: iuvmode is only set during IUV and UT runs
        # harness may or may not be defined
        if harness is None:
            # just skip the current testcase
            pytest.skip(line)
        elif harness.iuv is None:
            # UT: skip
            logger.err(f'ut: {msg}')
        else:
            harness.iuv.abort(line)
    else:
        # it's normal operation, end the pytest session
        # coverage: iuvmode is set for IUV and UT runs; never gets here
        pytest.exit(line)  # pragma: no cover
