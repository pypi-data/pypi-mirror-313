import json
import os
import re

import jsmin

from medver_pytest.lib.stdout_logger import StdoutLogger as logger


# -------------------
## Holds content for IUV requirements
class IUVRequirements:
    # -------------------
    ## constructor
    def __init__(self):
        ## path to the IUV requirements json file
        self._reqmts_path = os.path.join('iuv', 'iuv_srs.json')
        ## the IUV requirements
        self._reqmts = None

        ## path to the IUV trace json file
        self._trace_path = os.path.join('out', 'iuv', 'iuv_reqids.json')
        ## the IUV trace info
        self._trace = {}

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        with open(self._reqmts_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            self._reqmts = json.loads(cleanj)

        self.load_trace()

    # -------------------
    ## check the given reqid is valid
    #
    # @param reqid       the reqid to check
    # @param location    the location of the reqid
    # @return None if the reqid is ok, otherwise a message to print
    def check(self, reqid, location):
        msg = None
        # check reqid is named
        if reqid is None or reqid == '':
            msg = f'IUV: missing reqid: {location}'

        # check reqid is valid format
        if not re.search(r'^IUV-(\d+)', reqid):
            msg = f'IUV: bad reqid format: "{reqid}"'

        return msg

    # -------------------
    ## save iuv_verify() info to the trace json
    #
    # @param reqids    the reqid list for this call
    # @param result    whether the call passed or faild
    # @param location  the iuv_verify() location
    # @return None
    def save_reqids_to_trace(self, reqids, result, location):
        for reqid in reqids:
            if reqid not in self._trace:
                self._trace[reqid] = {
                    'passed': True,
                    'locations': [],
                }
            self._trace[reqid]['passed'] = result and self._trace[reqid]['passed']
            self._trace[reqid]['locations'].append(location)

        self.save_trace()

    # -------------------
    ## get desc for given requirement id
    #
    # @param reqid   the requirment id
    # @return description of the reqid
    def get(self, reqid):
        return self._reqmts[reqid]['desc']

    # -------------------
    ## load the trace file
    #
    # @return None
    def load_trace(self):
        if os.path.isfile(self._trace_path):
            with open(self._trace_path, 'r', encoding='utf-8') as fp:
                self._trace = json.load(fp)
        else:
            self._trace = {}

    # -------------------
    ## save trace content
    #
    # @return None
    def save_trace(self):
        if self._trace != {}:
            with open(self._trace_path, 'w', encoding='utf-8') as fp:
                json.dump(self._trace, fp, indent=4)

    # -------------------
    ## report summary of tested requirements and which passed/failed
    #
    # @param log_it  a callback function to write to the IUV log
    # @return None
    def report_trace(self, log_it):
        logger.line('IUV Report:')
        self.load_trace()

        results = self._trace

        total_tested_reqmts = 0
        total_tested_passed = 0
        total_passed_locations = 0
        total_tested_failed = 0
        total_failed_locations = 0
        results_keys = results.keys()
        for reqid in sorted(results_keys):
            info = results[reqid]
            total_tested_reqmts += 1
            if info['passed']:
                total_tested_passed += 1
                total_passed_locations += len(info['locations'])
            else:
                total_tested_failed += 1
                total_failed_locations += len(info['locations'])

        log_it('Total tested requirements', total_tested_reqmts, total_tested_reqmts)
        log_it('Total passed reqmts', total_tested_passed, total_tested_reqmts)
        log_it('Total passed locations', total_passed_locations)
        log_it('Total failed reqmts', total_tested_failed, total_tested_reqmts)
        log_it('Total failed locations', total_failed_locations)
        log_it('')

    # -------------------
    ## report list of IUV requirements that were not tested
    #
    # @param log_it  a callback function to write to the IUV log
    # @return None
    def report_missing(self, log_it):
        log_it('IUV Requirements not tested:')
        total_reqmts = 0
        total_tested = 0
        total_not_tested = 0
        for reqid in sorted(self._reqmts.keys()):
            total_reqmts += 1
            if reqid in self._trace.keys():
                total_tested += 1
            else:
                log_it(f'   {reqid: <8} {self.get(reqid)}')
                total_not_tested += 1

        if total_not_tested == 0:
            log_it('   None')

        log_it('')

        log_it('IUV Requirements summary:')
        log_it('Total requirements', total_reqmts, total_reqmts)
        log_it('Total tested', total_tested, total_reqmts)
        log_it('Total not tested', total_not_tested, total_reqmts)
        log_it('')
