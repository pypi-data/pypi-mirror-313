import argparse

from . import services


# -------------------
## handles CLI interface via conftest.py and normal argparse
class Cli:
    # -------------------
    ## initialize
    def __init__(self):
        ## holds true/false for running in IUV mode
        self.iuvmode = 'none'
        ## holds path to cfg.json file
        self.cfg_path = 'none'
        ## holds optional test run type; overrides cfg.json value
        self.test_run_type = 'none'
        ## holds optional test run id; overrides cfg.json value
        self.test_run_id = 'none'

    # -------------------
    ## conftest.py: add pytest options
    #
    # @param parser  the conftest parser object
    # @return None
    def addoption(self, parser):
        # note: use 'none' since default=None sets it to "None" not None
        parser.addoption('--iuvmode', action='store_true', dest='iuvmode', default='none')
        parser.addoption('--cfg_path', action='store', dest='cfg_path', default='none')
        parser.addoption('--test_run_type', action='store', dest='test_run_type', default='none')
        parser.addoption('--test_run_id', action='store', dest='test_run_id', default='none')

    # -------------------
    ## conftest.py: handle CLI overrides
    #
    # @param config  the conftest config object
    # @return None
    def configure(self, config):
        self.iuvmode = config.getoption('iuvmode')
        self.cfg_path = str(config.getoption('cfg_path'))

        self.test_run_type = config.getoption('test_run_type')
        self.test_run_id = config.getoption('test_run_id')

    # -------------------
    ## argparse: add cli arguments
    #
    # @return None
    def parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--iuvmode', action='store_true', dest='iuvmode', default='none')
        parser.add_argument('--cfg_path', action='store', dest='cfg_path', default='none')
        parser.add_argument('--test_run_type', action='store', dest='test_run_type', default='none')
        parser.add_argument('--test_run_id', action='store', dest='test_run_id', default='none')
        args, _ = parser.parse_known_args()

        self.iuvmode = args.iuvmode
        self.cfg_path = args.cfg_path
        self.test_run_type = args.test_run_type
        self.test_run_id = args.test_run_id

    # -------------------
    ## set values that are set i.e. non-overridable.
    # These are set before the cfg json file is read.
    #  * cfg_path
    #  * iuvmode
    #
    # @return None
    def save(self):
        # should only have non-overridable values in here
        if self.cfg_path != 'none':
            services.cfg.cfg_path = self.cfg_path
        if self.iuvmode != 'none':
            services.cfg.iuvmode = self.iuvmode

    # -------------------
    ## set values that override existing cfg values
    #  * test_run_type
    #  * test_run_id
    #
    # @return None
    def override(self):
        if self.test_run_type != 'none':
            services.cfg.test_run_type = self.test_run_type
        if self.test_run_id != 'none':
            services.cfg.test_run_id = self.test_run_id

    # -------------------
    ## check if a switch name is valid
    #
    # @param name   the switch name to check
    # @return True if valid, False otherwise
    def is_valid(self, name):
        return name in ['cfg_path', 'iuvmode', 'test_run_type', 'test_run_id']
