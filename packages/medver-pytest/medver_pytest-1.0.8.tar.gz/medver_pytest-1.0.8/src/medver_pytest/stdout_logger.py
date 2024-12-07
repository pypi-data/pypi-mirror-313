import sys


# -------------------
## Holds all info for logging debug lines
class StdoutLogger:
    ## flag to log to stdout or not
    verbose = True

    # --------------------
    ## log a message. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param msg     the message to print
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def log(ok, msg, prefix=None):
        if ok:
            StdoutLogger.ok(msg, prefix)
        else:
            StdoutLogger.err(msg, prefix)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param msgs    individual list of lines to print
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def log_all(ok, title, msgs, prefix=None):
        StdoutLogger.log(ok, f'{title}: {ok}', prefix)
        for msg in msgs:
            StdoutLogger.log(ok, f'   - {msg}', prefix)

    # -------------------
    ## write a "====" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def start(msg, prefix=None):
        StdoutLogger._write_line('====', msg, prefix)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def line(msg, prefix=None):
        StdoutLogger._write_line(' ', msg, prefix)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def ok(msg, prefix=None):
        StdoutLogger._write_line('OK', msg, prefix)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def err(msg, prefix=None):
        StdoutLogger._write_line('ERR', msg, prefix)

    # -------------------
    ## write a "bug" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def bug(msg, prefix=None):
        StdoutLogger._write_line('BUG', msg, prefix)

    # -------------------
    ## write an output line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def output(msg, prefix=None):
        StdoutLogger._write_line(' -- ', msg, prefix)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def warn(msg, prefix=None):
        StdoutLogger._write_line('WARN', msg, prefix)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def dbg(msg, prefix=None):
        StdoutLogger._write_line('DBG', msg, prefix)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag     the prefix tag
    # @param msg     the message to write
    # @param prefix  (optional) prefix for line
    # @return None
    @staticmethod
    def _write_line(tag, msg, prefix=None):
        if not StdoutLogger.verbose:
            return

        if prefix:
            print(f'{prefix} {tag: <4} {msg}')  # print okay
        else:
            print(f'{tag: <4} {msg}')  # print okay
        sys.stdout.flush()
