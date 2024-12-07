import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .gen_summary_base import GenSummaryBase
from ..common.gen_base_pdf import GenBasePdf
from ... import services
from ...constants import Constants


# -------------------
## Generates a Summary report in PDF format
class GenSummaryPdf(GenBasePdf, GenSummaryBase):
    # -------------------
    ## constructor
    #
    # @param summary    the summary data to use
    def __init__(self, summary):
        GenBasePdf.__init__(self)
        GenSummaryBase.__init__(self, summary)

        ## holds reference to the table being created
        self._tbl = None

        path = os.path.join(services.cfg.outdir, f'{Constants.summary_fname}.pdf')
        self._doc_init(path)

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        self._gen_test_run_details()
        self._gen_title('Summary')

        self._gen_req_summary()
        self._gen_proto_summary()

        self._build()

    # -------------------
    ## generate requirements summary
    #
    # @return None
    def _gen_req_summary(self):
        self._tbl = []
        self._tbl.append([
            Paragraph('<b>Requirements Summary</b>', self._style_sheet['BodyText'])
        ])

        # total requirements
        self._tbl.append(['', 'Count', 'Percentage'])

        # total requirements
        total = self._get_total_requirements()
        self._write_line('#Requirements', total, total)

        num_failing, num_passing, num_invalid, num_missing = self._count_requirements(total, self._report_invalid)
        self._write_line('   Invalid', num_invalid, total)
        self._write_line('   PASS', num_passing, total)
        self._write_line('   FAIL', num_failing, total)
        self._write_line('   Not tested', num_missing, total)

        self._gen_summary_table(self._tbl)

    # -------------------
    ## callback to report any invalid requirements
    #
    # @param reqid   the reqid to report as invalid
    # @return None
    def _report_invalid(self, reqid):
        msg = f'   {reqid} not found in {services.cfg.reqmt_json_path}'
        self._tbl.append([msg, '', ''])
        services.logger.warn(msg)

    # -------------------
    ## generate protocol summary
    #
    # @return None
    def _gen_proto_summary(self):
        self._tbl = []
        self._tbl.append([
            Paragraph('<b>Protocol Summary</b>', self._style_sheet['BodyText'])
        ])

        # total requirements
        self._tbl.append(['', 'Count', 'Percentage'])

        total = len(self._summary['protoids'])
        self._write_line('#Protocols', total, total)

        # count failing/passing reqmts
        num_failing, num_passing = self._count_protocols()
        self._write_line('   PASS', num_passing, total)
        self._write_line('   FAIL', num_failing, total)

        self._gen_summary_table(self._tbl)

    # -------------------
    ## write a line to table
    #
    # @param msg    the line header to write
    # @param count  the value to write
    # @param total  the total count
    # @return None
    def _write_line(self, msg, count, total):
        pct = self._pct(count, total)
        self._tbl.append([msg, count, pct])

    # -------------------
    ## generate a summary table
    #
    # @param tbl   the table to generate into
    # @return None
    def _gen_summary_table(self, tbl):
        tbl_widths = [
            3.20 * inch,  # desc
            0.50 * inch,  # value
            0.85 * inch,  # pct
        ]

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.25 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                # top row spans all columns
                ('BACKGROUND', (0, 0), (2, 0), colors.lightblue),
                ('SPAN', (0, 0), (2, 0)),

                # 2nd row is a title row
                ('BACKGROUND', (0, 1), (2, 1), colors.lightgrey),

                # "description" column is middle/center
                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),

                # "value" column is middle/right
                ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),

                # "%" column is middle/right
                ('VALIGN', (2, 0), (2, -1), 'MIDDLE'),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ]
        ))
        self._elements.append(t)
