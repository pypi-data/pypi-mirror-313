import reportlab.lib.pagesizes
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.platypus import Frame
from reportlab.platypus import PageTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from ... import services
from ...constants import Constants
from ...utils import Utils


# -------------------
## Base class for generating a PDF
class GenBasePdf:  # pylint: disable=too-few-public-methods

    # -------------------
    ## constructor
    def __init__(self):
        ## holds reference to the current PDF doc
        self._doc = None
        ## holds the list of style sheets for this doc
        self._style_sheet = None
        ## holds the current list of elements in the doc
        self._elements = []

        # uncomment to debug
        # services.logger.dbg(f"page_info: {services.cfg.page_info}")

    # -------------------
    ## initialize dcoument
    #
    # @param path   the path to the document
    # @return None
    def _doc_init(self, path):
        if services.cfg.page_info.page_size == 'letter':
            psize = reportlab.lib.pagesizes.LETTER
        elif services.cfg.page_info.page_size == 'a4':
            psize = reportlab.lib.pagesizes.A4
        else:
            services.abort(f'unknown page_size: {services.cfg.page_info.page_size}')
            return

        if services.cfg.page_info.orientation == 'portrait':
            self._doc = SimpleDocTemplate(path,
                                          pagesize=psize,
                                          leftMargin=0.5 * inch,
                                          rightMargin=0.5 * inch,
                                          topMargin=0.75 * inch,
                                          bottomMargin=1.0 * inch,
                                          )
        else:
            # landscape
            self._doc = SimpleDocTemplate(path,
                                          pagesize=landscape(psize),
                                          leftMargin=0.5 * inch,
                                          rightMargin=0.5 * inch,
                                          topMargin=0.75 * inch,
                                          bottomMargin=1.0 * inch,
                                          )

        self._style_sheet = getSampleStyleSheet()
        # set the overall font sizes
        # Normal is used for headers/footers
        self._style_sheet['Normal'].fontSize = 8
        # BodyText is used for all others
        self._style_sheet['BodyText'].fontSize = 8
        self._style_sheet.add(ParagraphStyle(name='ExtraSpace',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_LEFT,
                                             spaceAfter=5))
        self._style_sheet.add(ParagraphStyle(name='LeftPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_LEFT))
        self._style_sheet.add(ParagraphStyle(name='CenterPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_CENTER))
        self._style_sheet.add(ParagraphStyle(name='RightPara',
                                             parent=self._style_sheet['Normal'],
                                             alignment=TA_RIGHT))

        if services.cfg.page_info.orientation == 'portrait':
            self._style_sheet.add(ParagraphStyle(name='Mono',
                                                 parent=self._style_sheet['BodyText'],
                                                 alignment=TA_LEFT,
                                                 fontName='Courier-Bold',
                                                 fontSize=6
                                                 ))
        else:
            self._style_sheet.add(ParagraphStyle(name='Mono',
                                                 parent=self._style_sheet['BodyText'],
                                                 alignment=TA_LEFT,
                                                 fontName='Courier-Bold',
                                                 fontSize=6
                                                 ))

        self._elements = []
        frameh = Frame(self._doc.leftMargin,  # pylint: disable=no-member
                       self._doc.bottomMargin,  # pylint: disable=no-member
                       self._doc.width,
                       self._doc.height - 2 * cm,
                       id='normal')
        pt = PageTemplate(id='test', frames=[frameh], onPage=self._header_and_footer)
        self._doc.addPageTemplates([pt])

    # -------------------
    ## callback for generating header and footer on the given canvas
    #
    # @param canvas  the canvas to draw the header/footer into
    # @param doc     the doc
    # @return None
    def _header_and_footer(self, canvas, doc):
        self._header(canvas, doc)
        self._footer(canvas, doc)

    # -------------------
    ## callback for generating header on the given canvas
    #
    # @param canvas  the canvas to draw the header into
    # @param doc     the doc
    # @return None
    def _header(self, canvas, doc):
        canvas.saveState()
        edge_width = 1.75 * inch
        if services.cfg.page_info.orientation == 'portrait':
            t = Table([self._get_data('header', canvas)],
                      # should add to 7.5"
                      colWidths=[
                          edge_width,  # left
                          4.00 * inch,  # middle
                          edge_width,  # right
                      ],  # noqa
                      spaceBefore=0.1,
                      spaceAfter=0.1,
                      rowHeights=0.5 * inch,
                      )
        else:
            t = Table([self._get_data('header', canvas)],
                      # should add to 10"
                      colWidths=[
                          edge_width,  # left
                          6.50 * inch,  # middle
                          edge_width,  # right
                      ],  # noqa
                      spaceBefore=0.1,
                      spaceAfter=0.1,
                      rowHeights=0.5 * inch,
                      )

        t.setStyle(TableStyle(
            [
                # border below only
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
                # uncomment to get field delimiters in headers/footers
                # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        ))

        _, height = t.wrap(doc.width, doc.topMargin)
        t.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - height)
        canvas.restoreState()

    # -------------------
    ## callback for generating footer on the given canvas
    #
    # @param canvas  the canvas to draw the footer into
    # @param doc     the doc
    # @return None
    def _footer(self, canvas, doc):
        canvas.saveState()

        edge_width = 1.75 * inch
        if services.cfg.page_info.orientation == 'portrait':
            t = Table([self._get_data('footer', canvas)],
                      # should add to 7.5"
                      colWidths=[
                          edge_width,  # left
                          4.00 * inch,  # middle
                          edge_width,  # right
                      ],  # noqa
                      spaceBefore=0.0,
                      spaceAfter=0.0,
                      )
        else:
            t = Table([self._get_data('footer', canvas)],
                      # should add to 10"
                      colWidths=[
                          edge_width,  # left
                          6.50 * inch,  # middle
                          edge_width,  # right
                      ],  # noqa
                      spaceBefore=0.1,
                      spaceAfter=0.1,
                      rowHeights=0.5 * inch,
                      )

        t.setStyle(TableStyle(
            [
                # border below only
                ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
                # uncomment to get field delimiters in headers/footers
                # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        ))

        _, height = t.wrap(doc.width, doc.bottomMargin)
        t.drawOn(canvas, doc.leftMargin, height)

        canvas.restoreState()

    # -------------------
    ## callback for generating header/footer on the given canvas
    #
    # @param tag     the key into the cfg JSON object
    # @param canvas  the canvas to draw the footer into
    # @return the current row info for the header/footer
    def _get_data(self, tag, canvas):
        row = []
        if services.cfg.page_info[tag].left == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['LeftPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].left, self._style_sheet['LeftPara']))

        if services.cfg.page_info[tag].middle == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['CenterPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].middle, self._style_sheet['CenterPara']))

        if services.cfg.page_info[tag].right == '<pageno>':
            row.append(Paragraph(f'Page {canvas.getPageNumber()}', self._style_sheet['LeftPara']))
        else:
            row.append(Paragraph(services.cfg.page_info[tag].right, self._style_sheet['LeftPara']))

        return row

    # -------------------
    ## build the document with the current list of elements
    #
    # @return None
    def _build(self):
        self._doc.build(self._elements,
                        onFirstPage=self._header_and_footer,
                        onLaterPages=self._header_and_footer)

    # -------------------
    ## generate test run information
    #
    # @return None
    def _gen_test_run_details(self):
        para = Paragraph('<b>Test Run Details</b>', self._style_sheet['BodyText'])
        self._elements.append(para)

        line = f"{'Test Run Type': <20}: {services.cfg.test_run_type}"
        para = Paragraph(line, bulletText='\u2022')
        self._elements.append(para)

        line = f"{'Test Run ID': <20}: {services.cfg.test_run_id}"
        para = Paragraph(line, bulletText='\u2022')
        self._elements.append(para)

        dts = Utils.get_dts(use_cfg_fmt=True)
        line = f"{'Document Generated': <20}: {dts}"
        para = Paragraph(line, bulletText='\u2022')
        self._elements.append(para)

        line = f"{'medver-pytest version'}: v{Constants.version}"
        para = Paragraph(line, bulletText='\u2022')
        self._elements.append(para)

    # -------------------
    ## generate title
    #
    # @param title  the title to draw
    # @return None
    def _gen_title(self, title):
        para = Paragraph(f'<b>{title}</b>', self._style_sheet['BodyText'])
        self._elements.append(para)
