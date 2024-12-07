from ... import services
from ...constants import Constants
from ...utils import Utils


# -------------------
## Base class for generating an HTML with no meta, style, etc, tags
# useful for embedding the html into other HTML files
class GenBaseMinHtml:  # pylint: disable=too-few-public-methods

    # -------------------
    ## constructor
    def __init__(self):
        ## holds file pointer for the generated text file
        self._fp = None

    # -------------------
    ## generate test run information
    #
    # @return None
    def _gen_test_run_details(self):
        self._gen_title('Test Run Details')
        self._fp.write('<ul>\n')
        self._gen_li(f'Test Run Type: {services.cfg.test_run_type}')
        self._gen_li(f'Test Run ID: {services.cfg.test_run_id}')
        dts = Utils.get_dts(use_cfg_fmt=True)
        self._gen_li(f'Document Generated: {dts}')
        self._gen_li(f'medver-pytest version: v{Constants.version}')
        self._fp.write('</ul>\n')

    # -------------------
    ## generate title
    #
    # @param title  the title to draw
    # @param arg_id   option id= tag for the h3
    # @return None
    def _gen_title(self, title, arg_id=None):
        self._gen_h3(title, arg_id)

    # -------------------
    ## generate an h3 line
    #
    # @param text     the text to draw
    # @param arg_id   option id= tag for the h3
    # @return None
    def _gen_h3(self, text, arg_id=None):
        if arg_id is None:
            self._fp.write(f'<h3>{text}</h3>\n')
        else:
            self._fp.write(f'<h3 id="{arg_id}">{text}</h3>\n')

    # -------------------
    ## generate an paragraph highlighted and optionally indented
    #
    # @param text    the text to draw
    # @param indent  if true the text is indented
    # @return None
    def _gen_p_strong(self, text, indent=False):
        indent_str = ''
        if indent:
            indent_str = ' style="padding-left: 30px"'
        self._fp.write(f'<p{indent_str}><strong>{text}</strong></p>\n')

    # -------------------
    ## generate an li line
    #
    # @param text  the text to draw
    # @return None
    def _gen_li(self, text):
        self._fp.write(f'    <li>{text}</li>\n')

    # -------------------
    ## generate a table open tag
    #
    # @param css_class   optional CSS class to use for this table
    # @return None
    def _gen_table_open(self, css_class=None):
        if css_class is None:
            self._fp.write('<table>\n')
        else:
            self._fp.write(f'<table class="{css_class}">\n')

    # -------------------
    ## generates a end of table tag
    #
    # @returns None
    def _gen_table_close(self):
        self._fp.write('</table>\n')

    # -------------------
    ## generates a start of table heading section
    #
    # @returns None
    def _gen_thead_open(self):
        self._fp.write('    <thead>\n')

    # -------------------
    ## generates a end of table head tag
    #
    # @returns None
    def _gen_thead_close(self):
        self._fp.write('    </thead>\n')

    # -------------------
    ## generates a table body open definition
    #
    # @return None
    def _gen_tbody_open(self):
        self._fp.write('    <tbody>\n')

    # -------------------
    ## generates a end of table body tag
    #
    # @returns None
    def _gen_tbody_close(self):
        self._fp.write('    </tbody>\n')

    # -------------------
    ## generates a table row definition with the given class
    #
    # @param css_class  the CSS class to use
    # @returns None
    def _gen_tr_open(self, css_class=None):
        if css_class is None:
            self._fp.write('    <tr>\n')
        else:
            self._fp.write(f'    <tr class="{css_class}">\n')

    # -------------------
    ## generates a end of row tag
    #
    # @returns None
    def _gen_tr_close(self):
        self._fp.write('    </tr>\n')

    # -------------------
    ## generates a heading column definition
    #
    # @param text       the text to put in the title
    # @returns None
    def _gen_th_strong(self, text=None):
        if text is None:
            self._fp.write('        <th></th>\n')
        else:
            self._fp.write(f'        <th><strong>{text}</strong></th>\n')

    # -------------------
    ## generates a table heading definition with the given class
    #
    # @param text       the text to put in the title
    # @param css_class  the CSS class to use
    # @returns None
    def _gen_th(self, text=None, css_class=None):
        css_str = ''
        if css_class is not None:
            css_str = f' class="{css_class}"'

        if text is None:
            self._fp.write(f'        <th{css_str}></th>\n')
        else:
            self._fp.write(f'        <th{css_str}>{text}</th>\n')

    # -------------------
    ## generates a table column definition with the given class and highlighted
    #
    # @param text       the text to put in the title
    # @param css_class  the CSS class to use
    # @returns None
    def _gen_td_strong(self, text, css_class):
        if text is None:
            self._fp.write(f'        <td class="{css_class}"></td>\n')
        else:
            self._fp.write(f'        <td class="{css_class}"><strong>{text}</strong></td>\n')

    # -------------------
    ## generates a table column definition with the given class and optionally indented
    #
    # @param text       the text to put in the title
    # @param css_class  the CSS class to use
    # @param indent     if true, the text is indented
    # @returns None
    def _gen_td(self, text, css_class, indent=False):
        indent_str = ''
        if indent:
            indent_str = ' style="padding-left: 30px"'
        if text is None:
            self._fp.write(f'        <td class="{css_class}"{indent_str}></td>\n')
        else:
            self._fp.write(f'        <td class="{css_class}"{indent_str}>{text}</td>\n')

    # -------------------
    ## generates a table column definition indented and spanning multiple columns
    #
    # @param text   the text to put in the title
    # @param cols   the number of columns to span
    # @returns None
    def _gen_td_indented_spanned(self, text, cols):
        self._fp.write(f'<td colspan="{cols}" style="padding-left: 30px">{text}</td>\n')

    # -------------------
    ## generates a line break
    #
    # @returns None
    def _gen_blank_line(self):
        self._fp.write('<br/>\n')
