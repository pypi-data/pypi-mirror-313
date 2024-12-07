# -------------------
## Holds information used to format a value
class ResultFormatter(dict):
    # -------------------
    ## constructor
    def __init__(self):
        super().__init__()

        ## the tag to use for the actual value
        self.actual_tag = None

        ## flag indicating to format numeric value as hex
        self.as_hex = False

        ## user provided format to use
        self.format = None

    # TODO use json content in cfg.json to create a default formatter

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
