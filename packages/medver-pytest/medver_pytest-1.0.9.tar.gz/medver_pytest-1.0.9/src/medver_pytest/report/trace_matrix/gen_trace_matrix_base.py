from ... import services
from ...requirements import Requirements


# -------------------
## Common functions for Trace Matrix reports
class GenTraceMatrixBase:  # pylint: disable=too-few-public-methods
    # -------------------
    ## constructor
    #
    # @param matrix   the matrix info to use
    def __init__(self, matrix):
        ## holds reference to the matrix info
        self._matrix = matrix
        ## holds reference to the Requirents object
        self._requirements = None

    # -------------------
    ## initialization
    #
    # @return None
    def _gen_init(self):
        services.logger.start('report: trace matrix')

        self._requirements = Requirements()
        self._requirements.load()

    # -------------------
    ## add any extra reqmts in the test protocol data
    # to the requirement list
    #
    # @return None
    def _load_matrix_requirements(self):
        for req_id in self._matrix.keys():
            self._requirements.add_reqid(req_id)

    # -------------------
    ## iterates through all requirements and creates a row for each entry as needed
    #
    # @param report_header   callback to report a header line for this requirement
    # @param report_desc     callback to report the current requirement description
    # @param report_details  callback to report the details for this requirement
    # @return None
    def _report_requirements(self, report_header, report_desc, report_details):
        for req_id, reqmt in self._requirements.all_reqids():
            report_header(req_id, f'({reqmt["tester"]})')
            report_desc(reqmt['desc'])
            count = 0
            if req_id in self._matrix:
                for proto in sorted(self._matrix[req_id], key=lambda item: item['proto_id']):
                    report_details(proto['proto_id'], proto['proto_info'])
                    count += 1
                    if count > 35:
                        count = 0
                        # finish off current row
                        report_details(None, None)

                        # start a new one
                        report_header(req_id, f'({reqmt["tester"]})\n(cont\'d)')
                        report_desc(reqmt['desc'])

            if count == 0:
                if reqmt["tester"] == 'manual':
                    report_details(None, 'N/A')
                else:
                    report_details(None, '<b>ERR missing test case for this requirement</b>')

            # blank line or go to next row of the table
            report_details(None, None)
