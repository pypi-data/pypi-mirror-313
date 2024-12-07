from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable
from reportlab.platypus import ListItem
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .gen_tp_base import GenTpBase
from ..common.gen_base_pdf import GenBasePdf
from ... import services
from ...result_summary import ResultSummary


# -------------------
## Generates a Test Protocol report in PDF format
class GenTpPdf(GenBasePdf, GenTpBase):
    # -------------------
    ## constructor
    #
    # @param protocols   the data to use
    # @param do_results  generate results or not
    def __init__(self, protocols, do_results=True):
        ## see base clase for doc
        self._doc_path = None
        ## see base clase for doc
        self._testers = None

        GenBasePdf.__init__(self)
        GenTpBase.__init__(self, protocols, do_results)

        self._init('pdf', protocols, do_results)
        # uncomment to debug:
        # from medver_pytest.lib.stdout_logger import StdoutLogger as logger
        # logger.dbg(f'protocols: {json.dumps(self._protocols, indent=2)}')

        self._doc_init(self._doc_path)

        # === styles
        ## holds reference to the style sheet for most text in the doc
        self._stbody = self._style_sheet['BodyText']
        ## holds reference to the style sheet for text in a table row
        self._strow = self._style_sheet['BodyText']
        ## holds reference to the style sheet for text in monospace font
        self._stmono = self._style_sheet['Mono']

    # -------------------
    ## generate the report
    #
    # @return None
    def gen(self):
        self._gen_init()

        self._gen_test_run_details()
        title = self._get_title()
        self._gen_title(title)

        for _, protocol in self._protocols.items():
            self._gen_protocol(protocol)

        if self._testers:
            self._gen_testers()

        self._build()

    # -------------------
    ## generate a protocol table using the given data
    #
    # @param protocol   the data to use
    # @return None
    def _gen_protocol(self, protocol):
        tbl = []
        self._gen_protocol_info(tbl, protocol)

        requirements = []
        need_space = self._gen_steps_info(tbl, protocol['steps'], requirements)

        self._gen_protocol_table(tbl, need_space)
        self._gen_reqmt_table(requirements)

    # -------------------
    ## generate protocol info
    #
    # @param tbl        the table to write to
    # @param protocol   the data to use
    # @return None
    def _gen_protocol_info(self, tbl, protocol):
        if self._do_results:
            start_date = f'<b>Start date:</b>: {protocol["start_date"]}'
        else:
            start_date = '<b>Start date:</b>: '

        # row 0
        tbl.append([
            Paragraph(f'<b>{protocol["proto_id"]}</b>: {protocol["desc"]}', self._stbody),
            '', '', '',
            Paragraph(start_date, self._stbody),
            '', '',
        ])

        # row 1
        tbl.append([
            Paragraph(f'<b>At</b>: {protocol["location"]}', self._stbody),
            '', '', '',
            Paragraph('<b>Requirements:</b>: see below', self._stbody),
            '', '',
        ])

        # row 2
        tbl.append([
            Paragraph(f'<b>Software Version</b>: {protocol["dut_version"]}', self._stbody),
            '', '', '',
            Paragraph(f'<b>Serial number:</b> {protocol["dut_serialno"]}', self._stbody),
            '', '',
        ])

        # row 3
        tbl.append([
            self._gen_list('Objectives', protocol['objectives']),
            '', '', '', '', '',
        ])

        # row 4
        tbl.append([
            self._gen_list('Preconditions', protocol['preconditions']),
            '', '', '',
            self._gen_list('Deviations', protocol['deviations']),
            '', '',
        ])

    # -------------------
    ## generate a list using the given items
    #
    # @param tag      the name of the list
    # @param items    the list of data to use
    # @return a paragraph containing the formatted list
    def _gen_list(self, tag, items):
        paragraph_text = f'<b>{tag}</b>'
        if len(items) == 0:
            list_items = 'N/A'
            paragraph = Paragraph(f'{paragraph_text}: {list_items}', self._stbody)
        elif len(items) == 1:
            list_items = items[0]
            paragraph = Paragraph(f'{paragraph_text}: {list_items}', self._stbody)
        else:
            # more than 1 item in the list
            paragraph = [
                Paragraph(f'{paragraph_text}:', self._stbody),
            ]
            list_items = []
            for item in items:
                list_items.append(ListItem(Paragraph(item)))
            paragraph.append(ListFlowable(list_items, bulletType='bullet'))

        return paragraph

    # -------------------
    ## generate title row and one row per step
    #
    # @param tbl            the table to write to
    # @param steps          the steps data
    # @param requirements   the requirements found in all steps
    # @return None
    def _gen_steps_info(self, tbl, steps, requirements):
        # row 5: title row for step info
        tbl.append(
            [
                Paragraph('<b>Step</b>', self._stbody),
                Paragraph('<b>Req.</b>', self._stbody),
                Paragraph('<b>Execution Instructions</b>', self._stbody),
                Paragraph('<b>Expected</b>', self._stbody),
                Paragraph('<b>Actual</b>', self._stbody),
                Paragraph('<b>Pass /\nFail</b>', self._stbody),
                Paragraph('<b>Date</b>', self._stbody)
            ]
        )

        need_space = False
        if len(steps) == 0:
            tbl.append([Paragraph('N/A', self._strow), '', Paragraph('No steps found', self._strow), '', '', '', ''])
        else:
            # row N: one row for each step
            stepno = 0
            for step in steps:
                stepno += 1
                ns = self._gen_step(tbl, stepno, step, requirements)
                need_space = need_space or ns

        return need_space

    # -------------------
    ## generate a step in the test protocol
    #
    # @param tbl            the table to generate into
    # @param stepno         the step number of this step
    # @param step           the step description
    # @param requirements   the one or more reqids for this step
    # @return a paragraph containing the formatted list
    def _gen_step(self, tbl, stepno, step, requirements):
        # default is a passed, and empty result
        rs = ResultSummary()
        self._get_overall_result(step, rs)

        stepno = Paragraph(self._get_stepno('pdf', stepno), self._strow)
        reqids_str = Paragraph(self._get_reqids('pdf', rs, requirements), self._strow)
        desc = Paragraph(self._get_desc('pdf', step), self._strow)
        expected = Paragraph(self._get_expected('pdf', rs), self._stmono)
        actual = Paragraph(self._get_actual('pdf', rs), self._stmono)
        result = Paragraph(self._get_result('pdf', rs), self._strow)
        details = Paragraph(self._get_details('pdf', rs, step), self._strow)
        tbl.append([stepno, reqids_str, desc, expected, actual, result, details])

        if self._do_results:
            self._gen_step_comments(tbl, step)

        # if the actual or expected is long-ish, indicate those columsn will need more space
        if services.cfg.page_info.orientation == 'portrait':
            max_len = 10
        else:
            max_len = 20
        if len(str(rs.actual_formatted)) > max_len:
            return True
        if len(str(rs.expected_formatted)) > max_len:
            return True

        return False

    # -------------------
    ## generate the comments for the given step
    #
    # @param tbl    the table to add the comments to
    # @param step   the step data
    # @return None
    def _gen_step_comments(self, tbl, step):
        for comment in step['comments']:
            para = Paragraph(f'Note: {comment}', self._strow)
            tbl.append(['', '', para, '', '', '', ''])

    # -------------------
    ## generate a protocol table
    #
    # @param tbl          the table to draw into
    # @param need_space   indicates if the table requires a different format because of space layout
    # @return None
    def _gen_protocol_table(self, tbl, need_space):
        # these widths are the same portrait, landscape, needs space or not
        stepno_width = 0.41 * inch
        reqmt_width = 0.65 * inch
        details_width = 1.47 * inch
        result_width = 0.47 * inch
        if services.cfg.page_info.orientation == 'portrait':
            # portrait: should be 7.5"
            if need_space:
                value_width = 1.31 * inch
                tbl_widths = [
                    stepno_width,  # stepno
                    reqmt_width,  # reqmt.
                    1.88 * inch,  # desc
                    value_width,  # expected
                    value_width,  # actual
                    result_width,  # result
                    details_width,  # details
                ]
            else:
                value_width = 0.70 * inch
                tbl_widths = [
                    stepno_width,  # stepno
                    reqmt_width,  # reqmt.
                    3.10 * inch,  # desc
                    value_width,  # expected
                    value_width,  # actual
                    result_width,  # result
                    details_width,  # details
                ]
        else:
            # landscape (10" width)
            if need_space:
                value_width = 1.68 * inch
                tbl_widths = [
                    stepno_width,  # stepno
                    reqmt_width,  # reqmt.
                    3.64 * inch,  # desc
                    value_width,  # expected
                    value_width,  # actual
                    result_width,  # result
                    details_width,  # details
                ]
            else:
                value_width = 1.00 * inch
                tbl_widths = [
                    stepno_width,  # stepno
                    reqmt_width,  # reqmt.
                    5.00 * inch,  # desc
                    value_width,  # expected
                    value_width,  # actual
                    result_width,  # result
                    details_width,  # details
                ]

        # uncomment to debug
        # total = 0.0
        # for val in tbl_widths:
        #     total += val
        # # there are 72 per inch
        # logger.dbg(f"{total / 72: >8.2f} need_space:{need_space}")

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.25 * inch,
                  spaceAfter=0.0 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),

                # row 0: spans 2 cols, tp info and desc
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('SPAN', (0, 0), (4, 0)),
                ('SPAN', (4, 0), (-1, 0)),
                ('INNERGRID', (0, 0), (3, 0), 0.25, colors.black),

                # row 1: spans 2 cols, executed_by and requirements
                ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
                ('SPAN', (0, 1), (4, 1)),
                ('SPAN', (4, 1), (-1, 1)),

                # row 2: spans 2 cols, version and serialno
                ('BACKGROUND', (0, 2), (-1, 2), colors.lightblue),
                ('SPAN', (0, 2), (4, 2)),
                ('SPAN', (4, 2), (-1, 2)),

                # row 3: spans all cols, objectives
                ('BACKGROUND', (0, 3), (-1, 3), colors.lightblue),
                ('SPAN', (0, 3), (-1, 3)),

                # row 4: spans 2 cols, preconditions and deviations
                ('BACKGROUND', (0, 4), (-1, 4), colors.lightblue),
                ('SPAN', (0, 4), (4, 4)),
                ('SPAN', (4, 4), (-1, 4)),

                # use borders from now on
                # row 5: title row with all columns
                ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),

                # row 6 and on
                ('VALIGN', (0, 6), (0, -1), 'MIDDLE'),  # 0: stepno ; middle/center
                ('ALIGN', (0, 6), (0, -1), 'CENTER'),
                ('VALIGN', (1, 6), (1, -1), 'MIDDLE'),  # 1: reqmt
                ('VALIGN', (2, 6), (2, -1), 'MIDDLE'),  # 2: desc
                ('VALIGN', (3, 6), (3, -1), 'MIDDLE'),  # 3: expected
                ('VALIGN', (4, 6), (4, -1), 'MIDDLE'),  # 4: actual
                ('VALIGN', (5, 6), (5, -1), 'MIDDLE'),  # 5: result ; middle/center
                ('ALIGN', (5, 6), (5, -1), 'CENTER'),
                ('VALIGN', (6, 6), (6, -1), 'MIDDLE'),  # details
            ]
        ))
        self._elements.append(t)

    # -------------------
    ## generate a requirement table
    #
    # @param requirements   a list of reqmt info
    # @return None
    def _gen_reqmt_table(self, requirements):
        if services.cfg.page_info.orientation == 'portrait':
            # portrait: 7.5"
            tbl_widths = [
                0.85 * inch,  # reqmt.
                6.65 * inch,  # desc
            ]
        else:
            # landscape: 10"
            tbl_widths = [
                0.85 * inch,  # reqmt.
                9.15 * inch,  # desc
            ]

        # row 0: title row
        tbl = [
            [
                Paragraph('<b>Req.</b>', self._strow),
                Paragraph('<b>Desc.</b>', self._strow),
            ]
        ]

        if len(requirements) == 0:
            tbl.append([Paragraph('N/A', self._strow), Paragraph('No requirements found', self._strow)])
        else:
            for reqmt in sorted(requirements):
                reqmt_str = Paragraph(reqmt, self._strow)
                if reqmt in self._requirements:
                    desc = self._requirements[reqmt]['desc']
                else:
                    desc = f'Could not find {reqmt} in file: {services.cfg.reqmt_json_path}'
                tbl.append([reqmt_str, Paragraph(desc, self._strow)])

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.1 * inch,
                  spaceAfter=0.50 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),

                # use borders from now on
                # row 0: title row with all columns
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

                # row 1 and on
                ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),  # col 0: reqmt
                ('VALIGN', (1, 1), (1, -1), 'MIDDLE'),  # col 1: desc
            ]
        ))

        self._elements.append(t)

    # -------------------
    ## generate a tester signature area
    #
    # @return None
    def _gen_testers(self):
        para = Paragraph('<b>Manual Tester Signatures</b>', self._style_sheet['BodyText'])
        self._elements.append(para)

        if services.cfg.page_info.orientation == 'portrait':
            # portrait: 7.5"
            tbl_widths = [
                0.50 * inch,  # initials
                3.50 * inch,  # name
                3.50 * inch,  # signature
            ]
        else:
            # landscape: 10"
            tbl_widths = [
                0.50 * inch,  # initials
                3.25 * inch,  # name
                6.25 * inch,  # signature
            ]

        # row 0: title row
        tbl = [
            [
                Paragraph('<b></b>', self._strow),
                Paragraph('<b>Tester</b>', self._strow),
                Paragraph('<b>Signature</b>', self._strow),
            ]
        ]

        for initials in sorted(self._testers):
            if initials == 'manual':
                initials = ''
                name = ''
            elif initials in services.cfg.testers:
                name = services.cfg.testers[initials]
            else:
                name = ''
            tbl.append([Paragraph(initials, self._strow),
                        Paragraph(name, self._strow),
                        Paragraph('\n\n', self._strow)
                        ])

        t = Table(tbl,
                  colWidths=tbl_widths,
                  spaceBefore=0.1 * inch,
                  spaceAfter=0.50 * inch,
                  )

        t.setStyle(TableStyle(
            [
                # borders
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),

                # use borders from now on
                # row 0: title row with all columns
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

                # row 1 and on
                ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),  # col 0: initials
                ('VALIGN', (1, 1), (1, -1), 'MIDDLE'),  # col 1: name
                ('VALIGN', (1, 1), (1, -1), 'MIDDLE'),  # col 1: signature
            ]
        ))

        self._elements.append(t)
