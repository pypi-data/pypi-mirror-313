import json
import os

import jsmin

from . import services


# -------------------
## holds content of the requirements json file
class Requirements:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the requirements info from the json file, if any
        self._requirements = None
        ## indicates if the json file was found
        self._is_found = False
        ## indicates the total number of requirements
        self._total = 0
        ## indicates the number of requirements that are marked "auto"
        self._total_automated = 0
        ## indicates the number of requirements that are marked "manual"
        self._total_manual = 0
        ## indicates the number of requirements that are marked "both"
        self._total_both = 0

    # -------------------
    ## return whether the json file was found or not
    #
    # @return True if found, False otherwise
    @property
    def is_found(self):
        return self._is_found

    # -------------------
    ## total number of requirements in the file
    #
    # @return number of requirements
    @property
    def total(self):
        return self._total

    # -------------------
    ## total number of requirements marked "auto"
    #
    # @return number of automated requirements
    @property
    def total_automated(self):
        return self._total_automated

    # -------------------
    ## total number of requirements marked "manual"
    #
    # @return number of manual requirements
    @property
    def total_manual(self):
        return self._total_manual

    # -------------------
    ## total number of requirements marked "both"
    #
    # @return number of automated/manual requirements
    @property
    def total_both(self):
        return self._total_both

    # -------------------
    ## checks if the given requirement id is in the requirements list
    #
    # @param reqid  the id to check
    # @return True if the requirement is in the file
    def is_valid(self, reqid):
        return reqid in self._requirements

    # -------------------
    ## iterate through all requirements with a callback with reqid and reqmt info
    #
    # @return None
    def all_reqids(self):
        for reqid, reqmt in sorted(self._requirements.items()):
            yield reqid, reqmt

    # -------------------
    ## add a missing requirement, i.e. named in a protocol but not in the reqmt json file
    #
    # @param req_id  the requiremt id to add
    # @return None
    def add_reqid(self, req_id):
        if req_id in self._requirements:
            return

        if self._is_found:
            self._requirements[req_id] = {
                'tester': 'invalid',
                'desc': f'{req_id} not found in {services.cfg.reqmt_json_path}'
            }
        else:
            self._requirements[req_id] = {
                'tester': 'auto',
                'desc': 'N/A'
            }

    # -------------------
    ## load the json file
    #
    # @return None
    def load(self):
        if services.cfg.reqmt_json_path is None:
            self._requirements = {}
            return

        if not os.path.isfile(services.cfg.reqmt_json_path):
            services.logger.err(f'requirement json file not found: {services.cfg.reqmt_json_path}')
            self._requirements = {}
            return

        with open(services.cfg.reqmt_json_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            self._requirements = json.loads(cleanj)

        self._is_found = True

        self._total = 0
        self._total_automated = 0
        self._total_manual = 0
        self._total_both = 0
        for reqid, reqmt in self._requirements.items():
            if reqmt['tester'] == 'auto':
                self._total += 1
                self._total_automated += 1
            elif reqmt['tester'] == 'manual':
                self._total += 1
                self._total_manual += 1
            elif reqmt['tester'] == 'both':
                self._total += 1
                self._total_manual += 1
                self._total_automated += 1
                self._total_both += 1
            else:
                services.logger.err(f'{reqid}: found invalid "tester" value "{reqmt["tester"]}"')
                services.abort(f'invalid {services.cfg.reqmt_json_path}')

    # -------------------
    ## load the requirements json file
    #
    # @return None if not found or not set, otherwise the JSON content
    @staticmethod
    def fast_load():
        if services.cfg.reqmt_json_path is None:
            return {}

        if not os.path.isfile(services.cfg.reqmt_json_path):
            return {}

        with open(services.cfg.reqmt_json_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            return json.loads(cleanj)
