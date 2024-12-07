import os

from ... import services
from ...constants import Constants
from ...requirements import Requirements


# -------------------
## Common functions for TP reports
class GenTpBase:  # pylint: disable=too-few-public-methods
    # -------------------
    ## constructor
    #
    # @param protocols   the data to use
    # @param do_results  generate results or not
    def __init__(self, protocols, do_results):
        ## holds protocol inforation
        self._protocols = protocols
        ## holds flag to generate results (for TP report), or not (for TP doc)
        self._do_results = do_results

        ## holds requirements information
        self._requirements = []
        ## the path and file name of the generated document
        self._doc_path = None
        ## the extension of the document's file name
        self._doc_extension = None

        ## holds list of testers
        self._testers = []

    # -------------------
    ## initialization
    #
    # @param extension     the file name extension for the report file
    # @param protocols     the list of protocol objects for the report
    # @param do_results    flag indicating if it is (False) a test protocol or (True) a test report
    # @return None
    def _init(self, extension, protocols, do_results):
        ## holds protocol inforation
        self._protocols = protocols
        ## holds flag to generate results (for TP report), or not (for TP doc)
        self._do_results = do_results

        self._doc_extension = extension
        self._set_doc_path()

    # -------------------
    ## full document path
    #
    # @return None
    def _set_doc_path(self):
        if self._do_results:
            fname = Constants.tp_report_fname
        else:
            fname = Constants.tp_protocol_fname

        # hack
        if self._doc_extension == 'min-html':
            self._doc_path = os.path.join(services.cfg.outdir, f'{fname}-min.html')
        else:
            self._doc_path = os.path.join(services.cfg.outdir, f'{fname}.{self._doc_extension}')

    # -------------------
    ## initialization for generating the doc
    #
    # @return None
    def _gen_init(self):
        if self._do_results:
            services.logger.start(f'report: TP with results ({self._doc_extension})')
        else:
            services.logger.start(f'report: TP without results ({self._doc_extension})')

        self._requirements = Requirements.fast_load()

    # -------------------
    ## get the document title
    #
    # @return the title
    def _get_title(self):
        if self._do_results:
            title = 'Test Protocols with results'
        else:
            title = 'Test Protocols'
        return title

    # -------------------
    ## set the overall result (pass/fail) in the given result summary
    #
    # @param step   the current step object
    # @param rs     the current result summary object
    # @return None
    def _get_overall_result(self, step, rs):
        rs.passed()

        # start as passed, load each result
        # if they all passed, then display the last one
        # if any failed, then stop and display the first failed one
        # in all cases, the list of unique reqids in all results
        for res in step['results']:
            rs.append_result(res)
            if rs.result == 'FAIL':
                break

    # -------------------
    ## get the stepno ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param stepno   the current stepno
    # @return the formatted string
    def _get_stepno(self, doctype, stepno):  # pylint: disable=unused-argument
        return str(stepno)

    # -------------------
    ## get the step description ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param step     the current step
    # @return the formatted string
    def _get_desc(self, doctype, step):  # pylint: disable=unused-argument
        return str(step['desc'])

    # -------------------
    ## get the reqmt ids to print for the given document type
    #
    # @param doctype       the current document type
    # @param rs            the current result summary
    # @param requirements  a list of requirement ids found
    # @return the formatted string
    def _get_reqids(self, doctype, rs, requirements):
        # docx, txt
        if doctype in ['pdf', 'min-html']:
            delim = '<br/>'
        else:
            delim = '\n'

        if rs.reqids is None or rs.reqids == {}:
            reqids_str = 'N/A'
        else:
            for reqid in rs.reqids:
                if reqid not in requirements:
                    requirements.append(reqid)
            sorted_reqids = sorted(rs.reqids.keys())
            if len(sorted_reqids) == 1:
                reqids_str = sorted_reqids[0]
            else:
                reqids_str = delim.join(sorted_reqids)
        return reqids_str

    # -------------------
    ## get the expected value ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param rs       the result summary object
    # @return the formatted string
    def _get_expected(self, doctype, rs):
        if doctype in ['txt', 'docx']:
            val = str(rs.expected_formatted)
        else:
            # pdf, min-html: can have embedded html; to convert
            val = str(rs.expected_formatted).replace('<', '&lt;')
            val = val.replace('>', '&gt;')
        return val

    # -------------------
    ## get the actual value ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param rs       the result summary object
    # @return the formatted string
    def _get_actual(self, doctype, rs):
        val = ''
        if self._do_results:
            if doctype in ['txt', 'docx']:
                val = str(rs.actual_formatted)
            else:
                # pdf, min-html: can have embedded html; to convert
                val = str(rs.actual_formatted).replace('<', '&lt;')
                val = val.replace('>', '&gt;')

        return val

    # -------------------
    ## get the result (PASS/FAIL) ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param rs       the result summary object
    # @return the formatted string
    def _get_result(self, doctype, rs):  # pylint: disable=unused-argument
        val = ''
        if self._do_results:
            val = str(rs.result)
        return val

    # -------------------
    ## get the step details ready to print for the given document type
    #
    # @param doctype  the current document type
    # @param rs       the result summary object
    # @param step     the current step object
    # @return the formatted string
    def _get_details(self, doctype, rs, step):
        if doctype == 'docx':
            delim = '\n'
        elif doctype in ['pdf', 'min-html']:
            delim = '<br/>'
        else:
            delim = ', '

        if self._do_results:
            val = str(step['dts'])
        else:
            val = ''

        tester = step['tester']
        val += delim + 'tester: ' + tester
        if tester != 'auto':
            if tester not in self._testers:
                self._testers.append(tester)
        val += delim + str(rs.location)

        return val
