from .footer import Footer
from .header import Header
from ... import services


# -------------------
## Holds common page details
class PageDetails:
    # -------------------
    ## constuctor
    def __init__(self):
        ## holds the page orientation: portait or landscape
        self.orientation = 'portait'

        ## holds the page size: letter or A4
        self.page_size = 'letter'

        ## holds header info
        self.header = Header()

        ## holds footer info
        self.footer = Footer()

    # -------------------
    ## save a header item
    #
    # @param item    the name of the item to set: left, middle or right
    # @param value   the value to set
    # @return None
    def __setitem__(self, item, value):
        if item == 'orientation':
            self.orientation = value
            return

        if item == 'page_size':
            self.page_size = value
            return

        services.abort(f'bad item name: {item}')

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
