import json
import os

from medver_pytest.lib import services


# -------------------
## Holds content for IUV data as stored
# TODO handle other storage types
class IUVData:
    # -------------------
    ## constructor
    def __init__(self):
        pass

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        pass

    # -------------------
    ## load protocol JSON file
    #
    # @return json object
    def load_protocol(self):
        # TODO get the path from a common object e.g. harness
        path = os.path.join('out', 'iuv0', f'{services.cfg.test_script}_protocol.json')
        with open(path, 'r', encoding='utf=8') as fp:
            j = json.load(fp)
        return j

    # -------------------
    ## load trace JSON file
    #
    # @return json object
    def load_trace(self):
        # TODO get the path from a common object e.g. harness
        path = os.path.join('out', 'iuv0', f'{services.cfg.test_script}_trace.json')
        with open(path, 'r', encoding='utf=8') as fp:
            j = json.load(fp)
        return j

    # -------------------
    ## load summary JSON file
    #
    # @return json object
    def load_summary(self):
        # TODO get the path from a common object e.g. harness
        path = os.path.join('out', 'iuv0', f'{services.cfg.test_script}_summary.json')
        with open(path, 'r', encoding='utf=8') as fp:
            j = json.load(fp)
        return j
