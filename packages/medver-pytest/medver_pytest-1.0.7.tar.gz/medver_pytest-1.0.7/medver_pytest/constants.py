from .constants_version import ConstantsVersion


# -------------------
## Holds various constants
class Constants(ConstantsVersion):  # pylint: disable=too-few-public-methods
    ## trace document file name
    trace_fname = 'trace'

    ## summary document file name
    summary_fname = 'summary'

    ## test report document file name - with results
    tp_report_fname = 'test_report'

    ## test protocol document file name - no results
    tp_protocol_fname = 'test_protocol'
