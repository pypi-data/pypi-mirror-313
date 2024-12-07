import os

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .gen_trace_matrix_base import GenTraceMatrixBase
from ..common.gen_base_pdf import GenBasePdf
from ... import services
from ...constants import Constants


# -------------------
## Generates a Trace Matrix report in PDF format
class GenTraceMatrixPdf(GenBasePdf, GenTraceMatrixBase):
    # -------------------
    ## constructor
    #
    # @param matrix   the data to use
    def __init__(self, matrix):
        GenBasePdf.__init__(self)
        GenTraceMatrixBase.__init__(self, matrix)

        ## holds reference to the current table being generated
        self._tbl = None
        ## holds current reqmt id for the row
        self._row_id = None
        ## holds current reqmt info for the row
        self._row_info = None

        path = os.path.join(services.cfg.outdir, f'{Constants.trace_fname}.pdf')
        self._doc_init(path)

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        self._gen_test_run_details()
        self._gen_title('Trace Matrix')

        self._gen_trace_table()

        self._build()

    # -------------------
    ## generate a trace matrix table
    #
    # @return None
    def _gen_trace_table(self):
        self._tbl = []
        self._tbl.append(
            [
                Paragraph('<b>Req. Id</b>'),
                Paragraph('<b>Protocol</b>'),
            ]
        )

        self._load_matrix_requirements()
        ## see base class doc
        self._report_requirements(self._report_header, self._report_desc, self._report_details)

        self._gen_table()

    # -------------------
    ## callback to report the current requirement and tester info
    #
    # @param req_id   the requirement id to report
    # @param info     the info to report
    # @return None
    def _report_header(self, req_id, info):
        if self._row_id is not None:
            self._tbl.append([self._row_id, self._row_info])

        self._row_id = Paragraph(f'{req_id}\n{info}', self._style_sheet['CenterPara'])
        self._row_info = []

    # -------------------
    ## callback to report the current requirement's description (if available)
    #
    # @param desc     the description to report
    # @return None
    def _report_desc(self, desc):
        self._row_info.append(Paragraph(f'<i><b>Desc:</b> {desc}</i>',
                                        self._style_sheet['ExtraSpace']))

    # -------------------
    ## callback to report protocol id and info for the current requirement
    #
    # @param proto_id     the protocol id to report
    # @param proto_info   the protocol info to report
    # @return None
    def _report_details(self, proto_id, proto_info):
        if proto_id is None and proto_info is None:
            self._tbl.append([self._row_id, self._row_info])
            self._row_id = None
            self._row_info = None
        elif proto_id is None:
            self._row_info.append(Paragraph(f'{proto_info}',
                                            self._style_sheet['LeftPara']))
        else:
            self._row_info.append(Paragraph(f'{proto_id} {proto_info}',
                                            self._style_sheet['LeftPara']))

    # -------------------
    ## generate the trace matrix table
    #
    # @return None
    def _gen_table(self):
        tbl_widths = [
            0.75 * inch,  # reqid
            6.25 * inch,  # proto_info
        ]

        t = Table(self._tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.25 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                # top row is a title row
                ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),

                # "reqid" column
                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),

                # "protocol" column
                ('VALIGN', (1, 0), (1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ]
        ))
        self._elements.append(t)
