from .protocol.gen_tp_docx import GenTpDocx
from .protocol.gen_tp_minhtml import GenTpMinHtml
from .protocol.gen_tp_pdf import GenTpPdf
from .protocol.gen_tp_txt import GenTpTxt
from .summary.gen_summary_docx import GenSummaryDocx
from .summary.gen_summary_minhtml import GenSummaryMinHtml
from .summary.gen_summary_pdf import GenSummaryPdf
from .summary.gen_summary_txt import GenSummaryTxt
from .trace_matrix.gen_trace_matrix_docx import GenTraceMatrixDocx
from .trace_matrix.gen_trace_matrix_minhtml import GenTraceMatrixMinHtml
from .trace_matrix.gen_trace_matrix_pdf import GenTraceMatrixPdf
from .trace_matrix.gen_trace_matrix_txt import GenTraceMatrixTxt
from .. import services


# -------------------
## Generates all reports
# currently generates 3 types of reports:
#   * Protocol with results
#   * Trace matrix report
#   * Summary report
class Report:
    # -------------------
    ## constructor
    def __init__(self):
        pass

    # -------------------
    ## run all reports
    #
    # @return None
    def report(self):
        self._report_protocols()
        self._report_trace_matrix()
        self._report_summary()

    # -------------------
    ## run all protocol and reports
    #
    # @return None
    def _report_protocols(self):
        protocols = services.storage.get_protocols()

        # test protocol (no results): txt, pdf and docx
        services.cfg.page_info.set_tp_protocol_cfg()
        if 'txt' in services.cfg.report_types:
            rep = GenTpTxt(protocols, do_results=False)
            rep.gen()

        if 'pdf' in services.cfg.report_types:
            rep = GenTpPdf(protocols, do_results=False)
            rep.gen()

        if 'docx' in services.cfg.report_types:
            rep = GenTpDocx(protocols, do_results=False)
            rep.gen()

        if 'min-html' in services.cfg.report_types:
            rep = GenTpMinHtml(protocols, do_results=False)
            rep.gen()

        # reports with results: txt, pdf and docx
        services.cfg.page_info.set_tp_report_cfg()
        if 'txt' in services.cfg.report_types:
            rep = GenTpTxt(protocols, do_results=True)
            rep.gen()

        if 'pdf' in services.cfg.report_types:
            rep = GenTpPdf(protocols, do_results=True)
            rep.gen()

        if 'docx' in services.cfg.report_types:
            rep = GenTpDocx(protocols, do_results=True)
            rep.gen()

        if 'min-html' in services.cfg.report_types:
            rep = GenTpMinHtml(protocols, do_results=True)
            rep.gen()

    # -------------------
    ## run all trace matrix reports
    #
    # @return None
    def _report_trace_matrix(self):
        matrix = services.storage.get_trace()
        services.cfg.page_info.set_trace_cfg()

        if 'txt' in services.cfg.report_types:
            rep = GenTraceMatrixTxt(matrix)
            rep.gen()

        if 'pdf' in services.cfg.report_types:
            rep = GenTraceMatrixPdf(matrix)
            rep.gen()

        if 'docx' in services.cfg.report_types:
            rep = GenTraceMatrixDocx(matrix)
            rep.gen()

        if 'min-html' in services.cfg.report_types:
            rep = GenTraceMatrixMinHtml(matrix)
            rep.gen()

    # -------------------
    ## run all summary reports
    #
    # @return None
    def _report_summary(self):
        summary = services.storage.get_summary()
        services.cfg.page_info.set_summary_cfg()
        if 'txt' in services.cfg.report_types:
            rep = GenSummaryTxt(summary)
            rep.gen()

        if 'pdf' in services.cfg.report_types:
            rep = GenSummaryPdf(summary)
            rep.gen()

        if 'docx' in services.cfg.report_types:
            rep = GenSummaryDocx(summary)
            rep.gen()

        if 'min-html' in services.cfg.report_types:
            rep = GenSummaryMinHtml(summary)
            rep.gen()
