from .gen_tp_base import GenTpBase
from ..common.gen_base_minhtml import GenBaseMinHtml
from ... import services
from ...result_summary import ResultSummary


# -------------------
## Generates a Test Protocol report in min-html format
class GenTpMinHtml(GenBaseMinHtml, GenTpBase):
    # -------------------
    ## constructor
    #
    # @param protocols   the data to use
    # @param do_results  generate results or not (default True)
    def __init__(self, protocols, do_results=True):
        ## see base clase for doc
        self._doc_path = None

        GenBaseMinHtml.__init__(self)
        GenTpBase.__init__(self, protocols, do_results)

        self._init('min-html', protocols, do_results)

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
        ## see GenTpBase
        self._testers = []
        self._gen_protocol_info(protocol)

        requirements = []
        self._gen_steps_info(protocol['steps'], requirements)
        self._gen_reqmt_table(requirements)
        if self._testers:
            self._gen_blank_line()
            self._gen_testers()
        self._gen_blank_line()
        self._gen_blank_line()

    # -------------------
    ## generates the start of the steps table
    #
    # @returns None
    def _gen_steps_table_open(self):
        self._gen_table_open('ver-report-table')
        self._gen_thead_open()
        self._gen_tr_open(css_class='ver-report-steps-hdg')
        self._gen_th('Step', 'ver-report-steps-hdg-col1')
        self._gen_th('Req.', 'ver-report-steps-hdg-col2')
        self._gen_th('Execution Instructions', 'ver-report-steps-hdg-col3')
        self._gen_th('Expected', 'ver-report-steps-hdg-col4')
        self._gen_th('Actual', 'ver-report-steps-hdg-col5')
        self._gen_th('Pass / Fail', 'ver-report-steps-hdg-col6')
        self._gen_th('Date', 'ver-report-steps-hdg-col7')
        self._gen_tr_close()
        self._gen_thead_close()
        self._gen_tbody_open()

    # -------------------
    ## generates the end of the steps table
    #
    # @returns None
    def _gen_steps_table_close(self):
        self._gen_tbody_close()
        self._gen_table_close()

    # -------------------
    ## generate the overall protocol information
    #
    # @param protocol  the protocol data
    # @return None
    def _gen_protocol_info(self, protocol):
        self._gen_info_table_open()

        # row 0
        start_date = f'<strong>{"Start date": <17}</strong>: '
        if self._do_results:
            start_date += protocol["start_date"]
        self._gen_tr_open(css_class='ver-report-info1')
        self._gen_td(f'<strong>{protocol["proto_id"]}</strong>: {protocol["desc"]}', 'ver-report-info1-col1')
        self._gen_td(start_date, 'ver-report-info1-col2')
        self._gen_tr_close()

        # row 1
        self._gen_tr_open(css_class='ver-report-info1')
        self._gen_td(f'<strong>At</strong>: {protocol["location"]}', 'ver-report-info1-col1')
        self._gen_td('<strong>Requirements</strong> : see below', 'ver-report-info1-col2')
        self._gen_tr_close()

        # row 2
        self._gen_tr_open(css_class='ver-report-info1')
        self._gen_td(f'<strong>Software Version</strong>: {protocol["dut_version"]}', 'ver-report-info1-col1')
        self._gen_td(f'<strong>Serial number</strong>: {protocol["dut_serialno"]}', 'ver-report-info1-col2')
        self._gen_tr_close()

        # row 3
        self._gen_tr_open(css_class='ver-report-info2')
        fmt_str = self._get_list(protocol["objectives"])
        self._fp.write(f'<td colspan="2" class="ver-report-info2-col1"><strong>Objectives</strong>: {fmt_str}</td>\n')
        self._gen_tr_close()

        # row 4
        self._gen_tr_open(css_class='ver-report-info1')
        fmt_str = self._get_list(protocol["preconditions"])
        self._gen_td(f'<strong>Preconditions</strong>: {fmt_str}', 'ver-report-info1-col1')
        fmt_str = self._get_list(protocol["deviations"])
        self._gen_td(f'<strong>Deviations</strong>: {fmt_str}', 'ver-report-info1-col2')
        self._gen_tr_close()

        self._gen_info_table_close()

    # -------------------
    ## converts a list of items into an html unordered list
    # if the list is empty iit generates "N/A" text
    #
    # @param items   the list of items to include in the table
    # @returns None
    def _get_list(self, items):
        if len(items) == 0:
            fmt_list = 'N/A'
        else:
            fmt_list = '<ul>'
            for item in items:
                fmt_list += f'<li>{item}</li>'  # pylint: disable=consider-using-join
            fmt_list += '</ul>'
        return fmt_list

    # -------------------
    ## generates the start of the info table
    #
    # @returns None
    def _gen_info_table_open(self):
        self._gen_table_open('ver-report-table')
        self._gen_tbody_open()

    # -------------------
    ## generates the end of the info table
    #
    # @returns None
    def _gen_info_table_close(self):
        self._gen_tbody_close()
        self._gen_table_close()

    # -------------------
    ## generate title row and one row per step
    #
    # @param steps          the steps data
    # @param requirements   the requirements found in all steps
    # @return None
    def _gen_steps_info(self, steps, requirements):
        self._gen_steps_table_open()
        stepno = 0
        if len(steps) == 0:
            self._gen_tr_open()
            self._gen_td_indented_spanned('No steps found', 7)
            self._gen_tr_close()
        else:
            for step in steps:
                stepno += 1
                self._gen_step(stepno, step, requirements)
        self._gen_steps_table_close()

    # -------------------
    ## generate a step in the test protocol
    #
    # @param stepno         the step number of this step
    # @param step           the step description
    # @param requirements   the one or more reqids for this step
    # @return None
    def _gen_step(self, stepno, step, requirements):
        rs = ResultSummary()
        self._get_overall_result(step, rs)

        self._gen_tr_open()
        self._gen_td(self._get_stepno('min-html', stepno), css_class='ver-report-steps-col1')
        self._gen_td(self._get_reqids('min-html', rs, requirements), css_class='ver-report-steps-col2')
        self._gen_td(self._get_desc('min-html', step), css_class='ver-report-steps-col3')
        self._gen_td(self._get_expected('min-html', rs), css_class='ver-report-steps-col4')
        self._gen_td(self._get_actual('min-html', rs), css_class='ver-report-steps-col5')
        self._gen_td(self._get_result('min-html', rs), css_class='ver-report-steps-col6')
        self._gen_td(self._get_details('min-html', rs, step), css_class='ver-report-steps-col7')
        self._gen_tr_close()

        if self._do_results:
            self._gen_step_comments(step)

    # -------------------
    ## generate the comments for the given step
    #
    # @param step   the step data
    # @return None
    def _gen_step_comments(self, step):
        for comment in step['comments']:
            self._gen_tr_open()
            self._gen_td_indented_spanned(f'<strong>Note:</strong> {comment}', 7)
            self._gen_tr_close()

    # -------------------
    ## generate a requirement table
    #
    # @param requirements   a list of reqmt info
    # @return None
    def _gen_reqmt_table(self, requirements):
        self._gen_blank_line()
        self._gen_reqmts_table_open()
        if len(requirements) == 0:
            self._gen_tr_open()
            self._gen_td('N/A', css_class='ver-report-reqmts-col1')
            self._gen_td('No requirements found', css_class='ver-report-reqmts-col2')
            self._gen_tr_close()
        else:
            for reqmt in sorted(requirements):
                if reqmt in self._requirements:
                    desc = self._requirements[reqmt]['desc']
                else:
                    desc = f'Could not find {reqmt} in file: {services.cfg.reqmt_json_path}'

                self._gen_tr_open()
                self._gen_td(reqmt, css_class='ver-report-reqmts-col1')
                self._gen_td(desc, css_class='ver-report-reqmts-col2')
                self._gen_tr_close()
        self._gen_reqmts_table_close()

    # -------------------
    ## generates the start of the requirements table
    #
    # @returns None
    def _gen_reqmts_table_open(self):
        self._gen_table_open('ver-report-table')
        self._gen_thead_open()
        self._gen_tr_open(css_class='ver-report-hdg1')
        self._gen_th('Req.', 'ver-report-reqmts-hdg-col1')
        self._gen_th('Desc.', 'ver-report-reqmts-hdg-col2')
        self._gen_tr_close()
        self._gen_thead_close()
        self._gen_tbody_open()

    # -------------------
    ## generates the end of the requirements table
    #
    # @returns None
    def _gen_reqmts_table_close(self):
        self._gen_tbody_close()
        self._gen_table_close()

    # -------------------
    ## generate a signature area for all testers
    #
    # @return None
    def _gen_testers(self):
        self._gen_p_strong('Manual Tester Signatures', indent=True)

        self._gen_testers_table_open()
        for initials in sorted(self._testers):
            if initials == 'manual':
                initials = ''
                name = ''
            elif initials in services.cfg.testers:
                name = services.cfg.testers[initials]
            else:
                name = ''

            self._gen_tr_open()
            self._gen_td(initials, css_class='ver-report-testers-col1')
            self._gen_td(name, css_class='ver-report-testers-col2')
            self._gen_td('', css_class='ver-report-testers-col3')
            self._gen_tr_close()

        self._gen_testers_table_close()

    # -------------------
    ## generates the start of the testers table
    #
    # @returns None
    def _gen_testers_table_open(self):
        self._gen_table_open('ver-report-table')
        self._gen_thead_open()
        self._gen_tr_open(css_class='ver-report-hdg1')
        self._gen_th('', 'ver-report-testers-hdg-col1')
        self._gen_th('Tester', 'ver-report-testers-hdg-col2')
        self._gen_th('Signature', 'ver-report-testers-hdg-col3')
        self._gen_tr_close()
        self._gen_thead_close()
        self._gen_tbody_open()

    # -------------------
    ## generates the end of the testers table
    #
    # @returns None
    def _gen_testers_table_close(self):
        self._gen_tbody_close()
        self._gen_table_close()
