import tkinter as tk

from .dlg_manual_action import DlgManualAction
from .dlg_manual_verify import DlgManualVerify


# -------------------
## holds functions for displaying a GUI component for manual interactions
class Gui:
    # -------------------
    ## constructor
    def __init__(self):
        # create base window

        ## holds the base window
        self._root = tk.Tk()

        # disable 'x' button'
        self._root.overrideredirect(True)

        # make it invisible
        self._root.withdraw()

    # -------------------
    ## initialization
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

    # -------------------
    ## display a dialog box for a manual action to be performed by the tester
    #
    # @param proto_id   the test protocol id
    # @param action     the action for the tester to perform
    # @return None
    def show_step_action(self, proto_id, action):
        dlg = DlgManualAction()
        state, reason = dlg.step_manual_action(self._root,
                                               f'{proto_id}: perform manual action',
                                               action)
        return state, reason

    # -------------------
    ## display a dialog box for a manual action to be performed by the tester
    #
    # @param proto_id     the test protocol id
    # @param verify_desc  the verification for the tester to perform
    # @param expected     the expected value for the verification
    # @return None
    def show_verify(self, proto_id, verify_desc, expected):
        dlg = DlgManualVerify()
        state, actual = dlg.manual_verify(self._root,
                                          f'{proto_id}: perform manual verification',
                                          verify_desc,
                                          expected)
        return state, actual
