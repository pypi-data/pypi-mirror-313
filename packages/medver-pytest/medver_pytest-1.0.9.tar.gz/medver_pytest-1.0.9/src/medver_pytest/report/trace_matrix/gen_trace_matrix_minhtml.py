import os

from .gen_trace_matrix_base import GenTraceMatrixBase
from ..common.gen_base_minhtml import GenBaseMinHtml
from ... import services
from ...constants import Constants


# -------------------
## Generates a Trace Matrix report in min-html format
class GenTraceMatrixMinHtml(GenBaseMinHtml, GenTraceMatrixBase):
    # -------------------
    ## constructor
    #
    # @param matrix   the data to use
    def __init__(self, matrix):
        GenBaseMinHtml.__init__(self)
        GenTraceMatrixBase.__init__(self, matrix)

        ## holds path to the output file
        self._path = os.path.join(services.cfg.outdir, f'{Constants.trace_fname}-min.html')

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        with open(self._path, 'w', encoding='UTF-8') as self._fp:
            self._fp.write('<header id="ver-trace-title">\n')
            self._fp.write('    <h2 class="title">Trace Matrix</h2>\n')
            self._fp.write('</header>\n')
            self._fp.write('\n')

            self._gen_test_run_details()
            self._fp.write('\n')

            self._gen_title('Trace Matrix', arg_id='Matrix')
            self._load_matrix_requirements()
            self._gen_table_open(css_class='ver-trace-table')
            self._gen_thead_open()

            self._gen_tr_open(css_class='ver-trace-hdg1')
            self._gen_th('Req. Id', css_class='ver-trace-hdg-col1')
            self._gen_th('Protocol', css_class='ver-trace-hdg-col2')
            self._gen_tr_close()
            self._gen_thead_close()
            self._gen_tbody_open()
            ## see base class doc
            self._report_requirements(self._report_header, self._report_desc, self._report_details)
            self._gen_tbody_close()
            self._gen_table_close()

    # -------------------
    ## callback to report the current requirement and tester info
    #
    # @param req_id   the requirement id to report
    # @param info     the info to report
    # @return None
    def _report_header(self, req_id, info):
        # col1 of row
        self._fp.write('    <tr>\n')
        self._fp.write(f'        <td class="ver-trace-col1">{req_id}<br/>{info}</td>\n')

    # -------------------
    ## callback to report the current requirement's description (if available)
    #
    # @param desc     the description to report
    # @return None
    def _report_desc(self, desc):
        # col2, line1 of row
        self._fp.write('        <td class="ver-trace-col2">\n')
        self._fp.write(f'            <strong>Desc: </strong><em>{desc}</em><br/><br/>\n')

    # -------------------
    ## callback to report protocol id and info for the current requirement
    #
    # @param proto_id     the protocol id to report
    # @param proto_info   the protocol info to report
    # @return None
    def _report_details(self, proto_id, proto_info):
        # col2, line2 of row
        if proto_id is None and proto_info is None:
            self._fp.write('        </td>\n')
            self._fp.write('    </tr>\n')
        elif proto_id is None:
            self._fp.write(f'            <div>{proto_info}</div>\n')
        else:
            self._fp.write(f'            <div>{proto_id} {proto_info}</div>\n')
