import json
import os
import re

import jsmin

from . import services
from .build_info import BuildInfo
from .cli import Cli
from .constants import Constants
from .report.common.page_info import PageInfo


# -------------------
## Holds configuration functions and globals
class Cfg:
    # -------------------
    ## constructor
    def __init__(self):
        # --- Public - default settings
        # Note: order these for order in report()

        # == location of dirs and files
        ## holds path to cfg file
        self.cfg_path = None
        ## holds path to output directory
        self.outdir = 'out'
        ## holds path to directory holding status.json file
        self.statusdir = '.'
        ## holds path to the requirements json file
        self.reqmt_json_path = None

        # == test run related
        ## holds run type: one of formal, dryrun, dev
        self.test_run_type = 'dev'
        ## holds run id
        self.test_run_id = 'dev-001'

        ## report types to generate, valid: txt, pdf, docx, min-html
        self.report_types = ['txt', 'pdf', 'docx', 'min-html']
        ## report mode; use to suppress the creation of JSON files or not
        self.report_mode = False

        ## holds storage type: one of local, shared
        self.storage_type = 'local'
        ## holds path to the shared directory to publish; used only if storage_type is shared
        self.storage_shared_dir = None

        ## holds format to use for DTS
        self.dts_format = "%Y-%m-%d %H:%M:%S %Z"
        ## flag indicates to use UTC or local time
        self.use_utc = False

        # === skip these in report()

        ## holds page info e.g. headers and footers
        self.page_info = PageInfo()
        ## holds current test name
        self.test_script = None
        ## list of manual testers
        self.testers = []
        ## internal IUV use only; indicates if in IUV mode
        self.iuvmode = False

        ## holds reference to the CLI object
        self._cli = Cli()

    # -------------------
    ## add options for conftest.py behavior
    #
    # @param parser the pytest parser object
    # @return None
    def cli_addoption(self, parser):
        self._cli.addoption(parser)

    # -------------------
    ## handle the incoming CLI flags for conftest.py behavior
    #
    # @param config the pytest config reference
    # @return None
    def cli_configure(self, config):
        self._cli.configure(config)

    # -------------------
    ## add option for CLI behavior
    #
    # @return None
    def cli_parse(self):
        self._cli.parse()

    # -------------------
    ## used to set command line interface switches
    #
    # @param name   the name of the variable
    # @param value  the value of the variable to use
    # @return None
    def cli_set(self, name, value):
        if self._cli.is_valid(name):
            setattr(self, name, value)

    # -------------------
    ## initialize - step1
    # read cfg json file
    #
    # @param report_mode used to suppress creation of out/*.json files (for reporting)
    # @return None
    def init(self, report_mode):
        # save cfg_path and iuvmode if given on CLI
        self._cli.save()

        if self.iuvmode:
            services.harness.init_iuv()
            if self.cfg_path is None:
                # coverage: iuvmode is only set during IUV and UT runs
                # default to iuv/cfg0.json
                self.cfg_path = os.path.join('iuv', 'cfg0.json')

        # if still not set, default to cfg.json
        if self.cfg_path is None:
            self.cfg_path = 'cfg.json'

        self._read_ini()
        self.report_mode = report_mode

        # override any values given on CLI
        self._cli.override()

        if not os.path.isdir(self.outdir):  # pragma: no cover
            # coverage: in IUV and UT, outdir is created by scripts
            os.mkdir(self.outdir)

        self._check()

    # -------------------
    ## initialize - step2
    # get the current test name
    #
    # @return None
    def init2(self):
        self.test_script = None
        if 'PYTEST_CURRENT_TEST' in os.environ:  # pragma: no cover
            # coverage: in IUV and UT, variable is always set
            # e.g.  ver/test_sample_ver1.py
            m = re.search(r'test_(\w+)\.py::(\w+)', os.getenv('PYTEST_CURRENT_TEST'))
            if m:
                self.test_script = m.group(1)

    # -------------------
    ## report configuration to the log
    #
    # @return None
    def report(self):
        services.logger.start('Cfg:')
        for name, val in vars(self).items():
            self._log_attr(name, val)

        services.logger.line(f"  {'medver-pytest Version': <20}: {Constants.version}")
        services.logger.line(f"  {'git SHA': <20}: {BuildInfo.git_sha}")
        services.logger.line(f"  {'git Branch': <20}: {BuildInfo.git_branch}")
        services.logger.line(f"  {'git Uncommitted': <20}: {BuildInfo.git_uncommitted}")
        services.logger.line(f"  {'git Unpushed': <20}: {BuildInfo.git_unpushed}")

        services.logger.line('')

    # -------------------
    ## log configuration attribute
    #
    # @param name   the attribute name
    # @param val    the attribute value
    # @return None
    def _log_attr(self, name, val):
        if name.startswith('_'):
            # skip private attributes
            return

        if name == 'iuvmode' and not self.iuvmode:
            # only report if in iuvmode
            return

        if name in ['test_script', 'testers', 'page_info']:
            return

        if name == 'outdir':
            name = 'output_dir'
        elif name == 'statusdir':
            name = 'status_dir'

        elems = []
        for elem in name.split('_'):
            if elem in ['id', 'utc', 'json', 'dts']:
                elems.append(elem.upper())
            else:
                elems.append(elem.capitalize())

        nice_name = ' '.join(elems)
        services.logger.line(f'  {nice_name: <20}: {val}')

    # -------------------
    ## read the cfg json file
    # set attributes in this class based on content
    #
    # @return None
    def _read_ini(self):
        if not os.path.isfile(self.cfg_path):
            services.logger.warn(f'cfg_path "{self.cfg_path}" not found')
            return

        # load json file
        with open(self.cfg_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            j = json.loads(cleanj)

        # override and/or add to available attributes
        for key, value in j.items():
            if key == 'tp_report':
                self.page_info.init_tp_report(value)
            elif key == 'tp_protocol':
                self.page_info.init_tp_protocol(value)
            elif key == 'trace':
                self.page_info.init_trace(value)
            elif key == 'summary':
                self.page_info.init_summary(value)
            else:
                setattr(self, key, value)

    # -------------------
    ## checks all values for valid content
    # calls abort() if there are any failures
    #
    # @return None
    def _check(self):
        errs = 0
        errs += self.page_info.check()

        if self.cfg_path is None:
            errs += 1
            services.logger.err('cfg_path is None; must be a valid path to a cfg json file')

        if not os.path.isdir(self.outdir):
            errs += 1
            services.logger.err(f'outdir is not a valid dir; does it exist?: {self.outdir}')

        valid = ['local', 'shared']
        if self.storage_type not in valid:
            errs += 1
            services.logger.err(f'storage_type can only be {valid}, found: {self.storage_type}')
        elif self.storage_type == 'shared':
            if not os.path.isdir(self.storage_shared_dir):
                errs += 1
                services.logger.err(f'storage_shared_dir is not a valid dir; does it exist?: {self.storage_shared_dir}')

        # report_mode: nothing to check

        valid = ['formal', 'dryrun', 'dev']
        if self.test_run_type not in valid:
            errs += 1
            services.logger.err(f'test_run_type can only be {valid}, found: {self.test_run_type}')

        if self.test_run_id is None:
            errs += 1
            services.logger.err('test_run_id is None; must be a valid test run id')

        if self.dts_format is None:
            errs += 1
            services.logger.err('dts_format is None; must be a valid DTS format')
            # TODO check for other invalid formats. How?

        if self.use_utc is None:
            errs += 1
            services.logger.err('use_utc is None; must be True or False')

        # page_info: nothing to check
        # test_script: nothing to check
        # reqmt_json_path: nothing to check
        # tp_protocol_fname: nothing to check
        # tp_report_fname: nothing to check

        valid = ['txt', 'pdf', 'docx', 'min-html']
        if self.report_types is None:
            errs += 1
            services.logger.err('report_types is None; must be a list')
        elif not self.report_types:
            # allow an empty list
            pass
        else:
            # non-empty list, check all entries
            for rtype in self.report_types:
                if rtype not in valid:
                    errs += 1
                    services.logger.err(f'report_types can only be {valid}, found: {rtype}')

        if errs > 0:
            services.abort('cfg error found')
