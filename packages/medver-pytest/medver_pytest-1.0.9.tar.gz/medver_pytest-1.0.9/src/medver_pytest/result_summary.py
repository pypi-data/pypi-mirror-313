# -------------------
## Holds a result summary
class ResultSummary(dict):
    # -------------------
    ## constructor
    def __init__(self):
        super().__init__()
        ## the result so far: PASS/FAIL
        self.result = 'PASS'

        ## the raw actual value
        self.actual = None
        ## the original python type of the actual value
        self.actual_type = None
        ## the formatted string for display in the report of the actual value
        self.actual_formatted = None

        ## the raw expected value
        self.expected = None
        ## the original python type of the expected value
        self.expected_type = None
        ## the formatted string for display in the report of the expected value
        self.expected_formatted = None

        ## the list of reqids (if any) for this result
        self.reqids = None

        ## the verify_xx() location that generated this result
        self.location = None

        ## the formatter supplied by the user, if any
        self.formatter = None

    # -------------------
    ## load from a json object
    #
    # @param j   the json object
    # @return None
    def append_result(self, j):
        # overwrite these attributes
        self.result = j['result']
        self.actual = j['actual']
        self.actual_formatted = j['actual_formatted']
        self.actual_type = j['actual_type']
        self.expected = j['expected']
        self.expected_formatted = j['expected_formatted']
        self.expected_type = j['expected_type']
        self.location = j['location']
        self.formatter = j['formatter']

        # add on to the list of reqids
        if self.reqids is None:
            self.reqids = {}

        if j['reqids'] is None:
            pass
        else:
            for reqid in j['reqids'].keys():
                self.reqids[reqid] = 1

    # -------------------
    ## indicate this result has passed
    #
    # @return None
    def passed(self):
        self.result = 'PASS'

    # -------------------
    ## indicate this result has failed
    #
    # @return None
    def failed(self):
        self.result = 'FAIL'

    # -------------------
    ## set the reqids to the given list or string
    # Note: requirement ids are converted to upper case
    #
    # @param reqids   either None, a single string, a list of strings
    # @return None
    def set_reqids(self, reqids):
        if reqids is None:
            self.reqids = None
        elif isinstance(reqids, str):
            self.reqids = {reqids.upper(): 1}
        elif isinstance(reqids, list):
            self.reqids = {}
            for reqid in reqids:
                self.reqids[reqid.upper()] = 1

    # -------------------
    ## required for JSON to handle this class as a dictionary
    #
    # @param key      the name of the attribute to set
    # @param value    the value of the attribute
    # @return None
    def __setattr__(self, key, value):
        self[key] = value

    # -------------------
    ## required for JSON to handle this class as a dictionary
    #
    # @param key      the name of the attribute to get
    # @return the value of the named attribute
    def __getattr__(self, key):
        return self[key]

    # -------------------
    ## generate a formatted version of the actual value
    #
    # @param val    the value to format
    # @return None
    def format_actual(self, val):
        self.actual_type = type(val).__name__
        self.actual = str(val)
        if self.formatter is not None and self.formatter.actual_tag is not None:
            # override actual value with the tag the user requested
            self.actual_formatted = self.formatter.actual_tag
        else:
            formatted_val = self._format('format_actual', val, self.actual_type)
            self.actual_formatted = formatted_val

    # -------------------
    ## generate a formatted version of the expected value
    #
    # @param val      the value to format
    # @param prefix   (optional) string; a prefix on the formatted string
    # @param suffix   (optional) string; a suffix on the formatted string
    # @param is_not   (optional) bool; if True, add "not" as a prefix on the formatted string
    # @return None
    def format_expected(self, val, prefix=None, suffix=None, is_not=False):
        self.expected_type = type(val).__name__
        self.expected = str(val)
        if prefix is None:
            prefix = ''

        if suffix is None:
            suffix = ''

        if is_not:
            prefix = f'not {prefix}'

        formatted_val = self._format('format_expected', val, self.expected_type)
        self.expected_formatted = f'{prefix}{formatted_val}{suffix}'

    # -------------------
    ## generate a formatted version of the given regex
    #
    # @param val      the regex to format
    # @param is_not   (optional) bool; if True, add "not" as a prefix on the formatted string
    # @return None
    def format_regex_expected(self, val, is_not=False):
        self.expected_type = type(val).__name__
        self.expected = val
        if is_not:
            prefix = 'does not match'
        else:
            prefix = 'matches'
        self.expected_formatted = f'{prefix} r\'{str(val)}\''

    # -------------------
    ## generate a formatted version of the given delta
    #
    # @param val      the expected value to format
    # @param delta    numeric; the +/- value to use
    # @param is_pct   (optional) bool; if True, delta is percentage
    # @param is_not   (optional) bool; if True, add "outside" as a prefix on the formatted string
    # @return None
    def format_delta_expected(self, val, delta, is_pct=False, is_not=False):
        self.expected_type = type(val).__name__
        self.expected = val
        if is_not:
            prefix = 'outside '
        else:
            prefix = ''
        if is_pct:
            suffix = '%'
        else:
            suffix = ''
        self.expected_formatted = f'{prefix}{val} +/-{delta}{suffix}'

    # -------------------
    ## generate a formatted version of the given value
    #  no formatter: convert to string
    #  format given: generate string using the given format
    #  as_hex      : generate string using default hex format
    #
    # @param tag             used for logging purposes
    # @param val             the value to format
    # @param original_type   the python object type of the value
    # @return if successful a formatted string, otherwise None
    def _format(self, tag, val, original_type):
        if self.formatter is None:
            # no formatter, so just convert to a simple string
            return str(val)

        if self.formatter.format is not None:
            # user gave a format, so format it with their request
            return self.formatter.format % val

        if self.formatter.as_hex:
            return self._format_as_hex(tag, val, original_type)

        # formatter was supplied, but nothing to do,
        # so just convert to a simple string
        return str(val)

    # -------------------
    ## generate a formatted version of the given value as hex
    #   * int       : format as an 8 byte hex string
    #   * str       : convert to hex bytes
    #   * bytes     : format as a matrix of hex chars (as a string)
    #   * bytearray : format as a matrix of hex chars (as a string)
    #
    # @param tag             used for logging purposes
    # @param val             the value to format
    # @param original_type   the python object type of the value
    # @return if successful a formatted string, otherwise None
    def _format_as_hex(self, tag, val, original_type):  # pylint: disable=unused-argument
        if original_type == 'int':
            return f'0x{val:08X}'

        if original_type == 'str':
            val = bytes(val, "utf-8")

        if original_type in ['bytes', 'bytearray', 'str']:
            msg = ''
            count = 0
            for ch in val:
                count += 1
                if ch == val[-1]:
                    suffix = ''
                elif count == 8:
                    suffix = '\n'
                    count = 0
                else:
                    suffix = ' '
                msg += f'{ch:02X}{suffix}'
            return msg

        # nothing to do for this type,
        return str(val)
