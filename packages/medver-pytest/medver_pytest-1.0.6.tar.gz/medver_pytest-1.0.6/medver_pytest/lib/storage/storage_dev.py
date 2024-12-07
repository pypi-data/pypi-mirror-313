from .storage_file_base import StorageFileBase


# -------------------
## Holds storage information and how/where to save it
class StorageDev(StorageFileBase):
    # -------------------
    ## constructor
    def __init__(self):
        super().__init__()

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        pass

    # -------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass
