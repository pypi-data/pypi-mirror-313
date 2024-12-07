from . import services


# -------------------
## Holds data for the Summary report
class Summary:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the summary info
        self._summary = None
        ## holds the current test script name
        self._current_test_script = None
        ## indicates if there is any information to be saved to the output file
        self._dirty = False

        self._summary = {
            'reqids': {},
            'protoids': {},
        }

    # -------------------
    ## terminate - save all content
    #
    # @return None
    def term(self):
        self.save()

    # -------------------
    ## clear current summary content
    #
    # @return None
    def _clear(self):
        self._summary = {
            'reqids': {},
            'protoids': {},
        }
        self._dirty = True

    # -------------------
    ## ensure that the current data is cleared out when the test script changes
    #
    # @return None
    def check_test_script(self):
        # if the test script name has changed, save the current content and re-init protocols info
        if self._current_test_script != services.cfg.test_script:
            if self._current_test_script is not None:
                self.save()

            self._current_test_script = services.cfg.test_script
            self._clear()
            self._dirty = False

    # -------------------
    ## add a result info to the summary
    # save to storage
    #
    # @param reqids    list of requirement ids for this result
    # @param protoid   the protocol id for this result
    # @param result    the result info
    # @return None
    def add_result(self, reqids, protoid, result):
        self.check_test_script()

        if reqids is not None:
            for reqid in reqids:
                if reqid in self._summary['reqids']:
                    self._reqid_add_to(reqid, result)
                else:
                    self._reqid_add(reqid, result)

        if protoid in self._summary['protoids']:
            self._protoid_add_to(protoid, result)
        else:
            self._protoid_add(protoid, result)

        self.save()

    # -------------------
    ## add a reqid and result to the summary info
    #
    # @param reqid    rthe requirement id
    # @param result   the result i.e. PASS/FAIL
    # @return None
    def _reqid_add(self, reqid, result):
        self._summary['reqids'][reqid] = {
            'count': 1,
            'result': result
        }
        self._dirty = True

    # -------------------
    ## add result to an existing reqid info
    # if the current list is all PASS and the current result is a FAIL,
    # then the overall result is FAIL, otherwise the result remains as it was
    #
    # @param reqid    the requirement id
    # @param result   the result i.e. PASS/FAIL
    # @return None
    def _reqid_add_to(self, reqid, result):
        self._summary['reqids'][reqid]['count'] += 1
        if self._summary['reqids'][reqid]['result'] == 'PASS':
            self._summary['reqids'][reqid]['result'] = result
        # else if FAIL, stays FAIL

        self._dirty = True

    # -------------------
    ## add a protoid and result to the summary info
    #
    # @param protoid  the protocol id
    # @param result   the result i.e. PASS/FAIL
    # @return None
    def _protoid_add(self, protoid, result):
        self._summary['protoids'][protoid] = {
            'count': 1,
            'result': result
        }
        self._dirty = True

    # -------------------
    ## add result to an existing protoid info
    # if the current list is all PASS and the current result is a FAIL,
    # then the overall result is FAIL, otherwise the result remains as it was
    #
    # @param protoid   the protocol id
    # @param result    the result i.e. PASS/FAIL
    # @return None
    def _protoid_add_to(self, protoid, result):
        self._summary['protoids'][protoid]['count'] += 1
        if self._summary['protoids'][protoid]['result'] == 'PASS':
            self._summary['protoids'][protoid]['result'] = result
        # else if FAIL, stays FAIL

        self._dirty = True

    # -------------------
    ## save the summary info to storage
    #
    # @return None
    def save(self):
        services.storage.save_summary(self._summary)
        self._dirty = False

    # ===  IUV only

    # -------------------
    ## (IUV only) get current dirty flag
    #
    # @return dirty flag
    def iuv_get_dirty(self):
        return self._dirty

    # -------------------
    ## (IUV only) get summary object
    #
    # @return summary object
    def iuv_get_summary(self):
        return self._summary
