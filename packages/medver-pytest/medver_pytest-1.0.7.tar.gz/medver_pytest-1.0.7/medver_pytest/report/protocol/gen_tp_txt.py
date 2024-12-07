from .gen_tp_base import GenTpBase
from ..common.gen_base_txt import GenBaseTxt
from ... import services
from ...result_summary import ResultSummary


# -------------------
## Generates a Test Protocol report in text format
class GenTpTxt(GenBaseTxt, GenTpBase):
    # -------------------
    ## constructor
    #
    # @param protocols   the data to use
    # @param do_results  generate results or not (default True)
    def __init__(self, protocols, do_results=True):
        ## see base clase for doc
        self._doc_path = None
        ## see base clase for doc
        self._testers = None

        GenBaseTxt.__init__(self)
        GenTpBase.__init__(self, protocols, do_results)

        self._init('txt', protocols, do_results)

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()
        # uncomment to debug:
        # from medver_pytest.lib.stdout_logger import StdoutLogger as logger
        # logger.dbg(f'protocols: {json.dumps(self._protocols, indent=2)}')

        # TODO add data from self._requirements = Requirements.fast_load()

        with open(self._doc_path, 'w', encoding='UTF-8') as self._fp:
            self._gen_test_run_details()
            title = self._get_title()
            self._gen_title(title)

            for _, protocol in self._protocols.items():
                self._gen_protocol(protocol)

    # -------------------
    ## generate a protocol table using the given data
    #
    # @param protocol   the data to use
    # @return None
    def _gen_protocol(self, protocol):
        self._gen_protocol_info(protocol)

        requirements = []
        self._gen_steps_info(protocol['steps'], requirements)
        self._fp.write('\n')
        self._gen_reqmt_table(requirements)
        if self._testers:
            self._fp.write('\n')
            self._gen_testers()
        self._fp.write('\n\n')

    # -------------------
    ## generate the overall protocol information
    #
    # @param protocol  the protocol data
    # @return None
    def _gen_protocol_info(self, protocol):
        self._fp.write(f'==== protocol: {protocol["proto_id"]} {protocol["desc"]}\n')

        # row 0
        if self._do_results:
            start_date = f'     {"Start date": <17}: {protocol["start_date"]}\n'
        else:
            start_date = f'     {"Start date": <17}:\n'
        self._fp.write(start_date)

        # row 1
        self._fp.write(f'     {"At": <17}: {protocol["location"]}\n')
        self._fp.write(f'     {"Requirements": <17}: see below\n')

        # row 2
        self._fp.write(f'     {"Software Version": <17}: {protocol["dut_version"]}\n')
        self._fp.write(f'     {"Serial number": <17}: {protocol["dut_serialno"]}\n')

        # row 3
        self._fp.write(f'     {"Objectives": <17}: {protocol["objectives"]}\n')

        # row 4
        self._fp.write(f'     {"Preconditions": <17}: {protocol["preconditions"]}\n')
        self._fp.write(f'     {"Deviations": <17}: {protocol["deviations"]}\n')

    # -------------------
    ## generate title row and one row per step
    #
    # @param steps          the steps data
    # @param requirements   the requirements found in all steps
    # @return None
    def _gen_steps_info(self, steps, requirements):
        stepno = 0
        if len(steps) == 0:
            self._fp.write('     No steps found\n')
        else:
            for step in steps:
                stepno += 1
                self._gen_step(stepno, step, requirements)

    # -------------------
    ## generate a step in the test protocol
    #
    # @param stepno         the step number of this step
    # @param step           the step description
    # @param requirements   the one or more reqids for this step
    # @return None
    def _gen_step(self, stepno, step, requirements):
        self._fp.write(f'     Step {self._get_stepno("txt", stepno): <3}: {self._get_desc("txt", step)}\n')

        rs = ResultSummary()
        self._get_overall_result(step, rs)
        self._fp.write(f'       > reqids       : {self._get_reqids("txt", rs, requirements)}\n')
        self._fp.write(f'       > result       : {self._get_result("txt", rs)}\n')
        self._fp.write(f'       > expected     : {self._get_expected("txt", rs)}\n')
        self._fp.write(f'       > expected raw : {rs.expected}\n')
        self._fp.write(f'       > actual       : {self._get_actual("txt", rs)}\n')
        self._fp.write(f'       > actual raw   : {rs.actual}\n')
        self._fp.write(f'       > details      : {self._get_details("txt", rs, step)}\n')

        if self._do_results:
            self._gen_step_comments(step)

    # -------------------
    ## generate the comments for the given step
    #
    # @param step   the step data
    # @return None
    def _gen_step_comments(self, step):
        for comment in step['comments']:
            self._fp.write(f'       > Note         : {comment}\n')

    # -------------------
    ## generate a requirement table
    #
    # @param requirements   a list of reqmt info
    # @return None
    def _gen_reqmt_table(self, requirements):
        # row 0: title row
        self._fp.write(f'     {"Req.": <8} {"Desc.": <60}\n')
        self._fp.write(f'     {"-" * 8} {"-" * 60}\n')

        if len(requirements) == 0:
            self._fp.write(f'     {"N/A": <8} {"No requirements found"}\n')
        else:
            for reqmt in sorted(requirements):
                if reqmt in self._requirements:
                    desc = self._requirements[reqmt]['desc']
                else:
                    desc = f'Could not find {reqmt} in file: {services.cfg.reqmt_json_path}'

                self._fp.write(f'     {reqmt: <8} {desc}\n')

    # -------------------
    ## generate a signature area for all testers
    #
    # @return None
    def _gen_testers(self):
        self._fp.write('     Manual Tester Signatures\n')
        self._fp.write(f'     {"-" * 105}\n\n')

        self._fp.write(f'     {"": <3} {"Tester": <40} {"Signature": <60}\n')
        self._fp.write(f'     {"-" * 3} {"-" * 40} {"-" * 60}\n')

        for initials in sorted(self._testers):
            if initials == 'manual':
                initials = ''
                name = ''
            elif initials in services.cfg.testers:
                name = services.cfg.testers[initials]
            else:
                name = ''
            self._fp.write(f'\n     {initials: <3} {name: <40} {"_" * 60}\n')
