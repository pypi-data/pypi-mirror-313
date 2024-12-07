import os

from .gen_summary_base import GenSummaryBase
from ..common.gen_base_minhtml import GenBaseMinHtml
from ... import services
from ...constants import Constants


# -------------------
## Generates a Summary report in min-html format
class GenSummaryMinHtml(GenSummaryBase, GenBaseMinHtml):
    # -------------------
    ## constructor
    #
    # @param summary    the summary data to use
    def __init__(self, summary):
        GenBaseMinHtml.__init__(self)
        GenSummaryBase.__init__(self, summary)

        ## holds path to the output file
        self._path = os.path.join(services.cfg.outdir, f'{Constants.summary_fname}-min.html')

        ## holds file pointer to the output file
        self._fp = None

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        with open(self._path, 'w', encoding='UTF-8') as self._fp:
            self._fp.write('<header id="ver-summary-title">\n')
            self._fp.write('    <h2 class="title">Automated Test Summary</h2>\n')
            self._fp.write('</header>\n')
            self._fp.write('\n')

            self._gen_test_run_details()
            self._fp.write('\n')

            self._gen_title('Summary', arg_id='Summary')
            self._gen_req_summary()
            self._gen_blank_line()
            self._gen_proto_summary()

    # -------------------
    ## generate requirements summary
    #
    # @return None
    def _gen_req_summary(self):
        self._gen_section_open('Requirements Summary')

        # TODO @@@ NEW table?
        # total requirements
        if self._requirements.is_found:
            total = self._requirements.total
            self._write_row('#Requirements', total, total)

            count = self._requirements.total_manual
            self._write_row('Manual Requirements', count, total)

            count = self._requirements.total_both
            self._write_row('Manual & Auto Requirements', count, total)

            total = self._requirements.total_automated
        else:
            total = len(self._summary['reqids'])

        self._write_row('Automated Requirements', total, total)

        # count failing/passing reqmts
        num_failing, num_passing, num_invalid, num_missing = self._count_requirements(total, self._report_invalid)
        self._write_row('Invalid', num_invalid, total, indent=True)
        self._write_row('PASS', num_passing, total, indent=True)
        self._write_row('FAIL', num_failing, total, indent=True)
        self._write_row('Not tested', num_missing, total, indent=True)

        self._gen_section_close()

    # -------------------
    ## callback to report any invalid requirements
    #
    # @param reqid  the reqid to report
    # @return None
    def _report_invalid(self, reqid):
        msg = f'   {reqid} not found in {services.cfg.reqmt_json_path}'
        services.logger.warn(msg)
        self._fp.write(f'{msg}\n')

    # -------------------
    ## generate protocol summary
    #
    # @return None
    def _gen_proto_summary(self):
        self._gen_section_open('Protocol Summary')

        # total protocols
        total = len(self._summary['protoids'])
        self._write_row('#Protocols', total, total)

        # count failing/passing reqmts
        num_failing, num_passing = self._count_protocols()
        self._write_row('PASS', num_passing, total, indent=True)
        self._write_row('FAIL', num_failing, total, indent=True)

        self._gen_section_close()

    # -------------------
    ## generates the start of a sections table
    #
    # @param title   the title of the table
    # @returns None
    def _gen_section_open(self, title):
        self._gen_table_open(css_class='ver-summary-table')
        # heading1
        self._gen_thead_open()
        self._gen_tr_open(css_class='ver-summary-hdg1')
        self._gen_th_strong(title)
        self._gen_th_strong()
        self._gen_th_strong()
        self._gen_tr_close()
        self._gen_thead_close()

        self._gen_tbody_open()
        # heading2
        self._gen_tr_open(css_class='ver-summary-hdg2')
        self._gen_td_strong(text=None, css_class='ver-summary-hdg-col1')
        self._gen_td_strong('Count', css_class='ver-summary-hdg-col2')
        self._gen_td_strong('Percentage', css_class='ver-summary-hdg-col3')
        self._gen_tr_close()

    # -------------------
    ## closes body and table of the current summary section
    #
    # @returns None
    def _gen_section_close(self):
        self._gen_tbody_close()
        self._gen_table_close()

    # -------------------
    ## write a row to the given file
    #
    # @param msg         the line header to write
    # @param count       the value to write
    # @param total       the total count
    # @param css_class   the css class to associated with this row
    # @param indent      if true, indent the first column
    # @return None
    def _write_row(self, msg, count, total, css_class=None, indent=False):
        pct = self._pct(count, total).strip()

        self._gen_tr_open(css_class)
        self._gen_td(msg, css_class='ver-summary-col1', indent=indent)
        self._gen_td(count, css_class='ver-summary-col2')
        self._gen_td(pct, css_class='ver-summary-col3')
        self._gen_tr_close()
