import os

from .gen_summary_base import GenSummaryBase
from ..common.gen_base_txt import GenBaseTxt
from ... import services
from ...constants import Constants


# -------------------
## Generates a Summary report in text format
class GenSummaryTxt(GenSummaryBase, GenBaseTxt):
    # -------------------
    ## constructor
    #
    # @param summary    the summary data to use
    def __init__(self, summary):
        GenBaseTxt.__init__(self)
        GenSummaryBase.__init__(self, summary)

        ## holds path to the output file
        self._path = os.path.join(services.cfg.outdir, f'{Constants.summary_fname}.txt')

        ## holds file pointer to the output file
        self._fp = None

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        with open(self._path, 'w', encoding='UTF-8') as self._fp:
            self._gen_test_run_details()
            self._gen_title('Summary')

            self._gen_req_summary()
            self._fp.write('\n')
            self._gen_proto_summary()

    # -------------------
    ## generate requirements summary
    #
    # @return None
    def _gen_req_summary(self):
        # total requirements
        if self._requirements.is_found:
            total = self._requirements.total
            self._write_line('#Requirements', total, total)

            count = self._requirements.total_manual
            self._write_line('Manual Requirements', count, total)

            count = self._requirements.total_both
            self._write_line('Manual & Auto Requirements', count, total)

            total = self._requirements.total_automated
        else:
            total = len(self._summary['reqids'])

        self._write_line('Automated Requirements', total, total)

        # count failing/passing reqmts
        num_failing, num_passing, num_invalid, num_missing = self._count_requirements(total, self._report_invalid)
        self._write_line('   Invalid', num_invalid, total)
        self._write_line('   PASS', num_passing, total)
        self._write_line('   FAIL', num_failing, total)
        self._write_line('   Not tested', num_missing, total)

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
        # total protocols
        total = len(self._summary['protoids'])
        self._write_line('#Protocols', total, total)

        # count failing/passing reqmts
        num_failing, num_passing = self._count_protocols()
        self._write_line('   PASS', num_passing, total)
        self._write_line('   FAIL', num_failing, total)

    # -------------------
    ## write a line to the given file
    #
    # @param msg    the line header to write
    # @param count  the value to write
    # @param total  the total count
    # @return None
    def _write_line(self, msg, count, total):
        pct = self._pct(count, total)
        self._fp.write(f'{msg: <27}: {count: >3}  {pct}\n')
