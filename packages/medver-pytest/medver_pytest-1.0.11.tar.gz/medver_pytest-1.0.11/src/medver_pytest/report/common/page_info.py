from .footer import Footer
from .header import Header
from .page_details import PageDetails
from ... import services


# -------------------
## holds page information for generating documents
class PageInfo:

    # -------------------
    ## constructor
    def __init__(self):
        ## the page orientation: landscape or portrait
        self.orientation = 'landscape'

        ## the page size: letter or a4
        self.page_size = 'letter'

        ## the header info
        self.header = Header()

        ## the footer info
        self.footer = Footer()

        ## the test report page details
        self._tp_report = PageDetails()
        ## default orientation for test report is landscapte
        self._tp_report.orientation = 'landscape'

        ## the test protocol results page details
        self._tp_protocol = PageDetails()
        ## default orientation for test protocol results is landscapte
        self._tp_protocol.orientation = 'landscape'

        ## the trace matrix page details
        self._trace = PageDetails()
        ## default orientation for trace matrix is landscapte
        self._trace.orientation = 'landscape'

        ## the summary page details
        self._summary = PageDetails()
        ## default orientation for trace matrix is portrait
        self._trace.orientation = 'portrait'

    # -------------------
    ## get a value from this object
    #
    # @param item   the name of the attribute to get
    # @return the value of the attribute
    def __getitem__(self, item):
        if item == 'header':
            return self.header

        if item == 'footer':
            return self.footer

        if item == 'orientation':
            return self.orientation

        if item == 'page_size':
            return self.page_size

        services.abort(f'bad item name: {item}')
        return None  # for lint

    # -------------------
    ## initialize all test protocol (no results) fields
    #
    # @param item  the value to set
    # @return None
    def init_tp_protocol(self, item):
        self._set_all_fields(item, self._tp_protocol)

    # -------------------
    ## initialize all test report (with results) with results fields
    #
    # @param item  the value to set
    # @return None
    def init_tp_report(self, item):
        self._set_all_fields(item, self._tp_report)

    # -------------------
    ## initialize all trace matrix fields
    #
    # @param item  the value to set
    # @return None
    def init_trace(self, item):
        self._set_all_fields(item, self._trace)

    # -------------------
    ## initialize all summary fields
    #
    # @param item  the value to set
    # @return None
    def init_summary(self, item):
        self._set_all_fields(item, self._summary)

    # -------------------
    ## initialize all test protocol (no results) cfg to default values
    #
    # @return None
    def set_tp_protocol_cfg(self):
        self._set_all_cfg(self._tp_protocol)

    # -------------------
    ## initialize all test report with results cfg to default values
    #
    # @return None
    def set_tp_report_cfg(self):
        self._set_all_cfg(self._tp_report)

    # -------------------
    ## initialize all trace matrix cfg to default values
    #
    # @return None
    def set_trace_cfg(self):
        self._set_all_cfg(self._trace)

    # -------------------
    ## initialize all summary cfg to default values
    #
    # @return None
    def set_summary_cfg(self):
        self._set_all_cfg(self._summary)

    # -------------------
    ## check some content
    #
    # @return number of errors found
    def check(self):
        errs = 0
        if self._tp_protocol.orientation != self._tp_report.orientation:
            errs += 1
            services.logger.err(f'tp_protocol orientation ({self._tp_protocol.orientation}) '
                                f'does not match tp_report ({self._tp_report.orientation})')

        return errs

    # -------------------
    ## generate a report to the given file
    #
    # @param fp  the file to write to
    # @return None
    def report(self, fp):
        fp.write(f"{'Header left': <20}: {self.header.left}\n")
        fp.write(f"{'Header middle': <20}: {self.header.middle}\n")
        fp.write(f"{'Header right': <20}: {self.header.right}\n")

        fp.write(f"{'Footer left': <20}: {self.footer.left}\n")
        fp.write(f"{'Footer middle': <20}: {self.footer.middle}\n")
        fp.write(f"{'Footer right': <20}: {self.footer.right}\n")

    # === Private

    # -------------------
    ## set the current values from the given source
    #
    # @param src   the source to use
    # @return None
    def _set_all_cfg(self, src):
        self.orientation = src.orientation
        self.page_size = src.page_size

        self.header.left = src.header.left
        self.header.middle = src.header.middle
        self.header.right = src.header.right

        self.footer.left = src.footer.left
        self.footer.middle = src.footer.middle
        self.footer.right = src.footer.right

    # -------------------
    ## set the various fields
    # * orientation
    # * page size
    # * headder: left, middle, right
    # * footer : left, middle, right
    #
    # @param src   the source to use
    # @param dst   the destinaton to save to
    # @return None
    def _set_all_fields(self, src, dst):
        self._set_field(src, dst, 'orientation')
        self._set_field(src, dst, 'page_size')
        self._set_sub_field(src, dst, 'header', 'left')
        self._set_sub_field(src, dst, 'header', 'middle')
        self._set_sub_field(src, dst, 'header', 'right')
        self._set_sub_field(src, dst, 'footer', 'left')
        self._set_sub_field(src, dst, 'footer', 'middle')
        self._set_sub_field(src, dst, 'footer', 'right')

    # -------------------
    ## set a destination field from the source
    #
    # @param src     the source to use
    # @param dst     the destinaton to save to
    # @param field   the field name
    # @return None
    def _set_field(self, src, dst, field):
        if field in src:
            dst[field] = src[field]

    # -------------------
    ## set a destination subfield from the source
    #
    # @param src     the source to use
    # @param dst     the destinaton to save to
    # @param parent  the parent field
    # @param field   the subfield name
    # @return None
    def _set_sub_field(self, src, dst, parent, field):
        if field in src[parent]:
            dst[parent][field] = src[parent][field]
