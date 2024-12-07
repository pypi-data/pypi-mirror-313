from ... import services


# -------------------
## holds Footer information
class Footer:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds content for left side of footer
        self.left = ''

        ## holds content for center section of footer
        self.middle = ''

        ## holds content for right side of footer
        self.right = ''

    # -------------------
    ## save a footer item
    #
    # @param item    the name of the item to set: left, middle or right
    # @param value   the value to set
    # @return None
    def __setitem__(self, item, value):
        if item == 'left':
            self.left = value
            return

        if item == 'middle':
            self.middle = value
            return

        if item == 'right':
            self.right = value
            return

        services.abort(f'bad item name: {item}')

    # -------------------
    ## get a value from this object
    #
    # @param item   the name of the attribute to get
    # @return the value of the attribute
    def __getitem__(self, item):
        if item == 'left':
            return self.left

        if item == 'middle':
            return self.middle

        if item == 'right':
            return self.right

        services.abort(f'bad item name: {item}')
        return None
