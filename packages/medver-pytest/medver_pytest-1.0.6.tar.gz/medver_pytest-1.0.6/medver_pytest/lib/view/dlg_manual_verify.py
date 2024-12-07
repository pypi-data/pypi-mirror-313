import tkinter as tk
import tkinter.scrolledtext as tkst

from .dlg_base import DlgBase
from .. import services


# -------------------
## holds Dialog Box for a Manual Verify
class DlgManualVerify(DlgBase):
    # -------------------
    ## constructor
    def __init__(self):
        ## see base class for doc
        self._dlg = None

        super().__init__()

        ## the return state, holds abort, pass, or fail
        self._return_value = 'initial'
        ## the actual value that occurred, cannot be ''
        self._actual = ''
        ## whether actual was ever entered or not
        self._actual_entered = False

        # widgets
        ## the Pass btn
        self._btn_pass = None
        ## the Fail btn
        self._btn_fail = None
        ## the Actual Text widget
        self._txt_actual = None

    # -------------------
    ## show dialog for a manual verify
    #
    # @param parent   the tk root window
    # @param title    the dlg title
    # @param verify_desc   the action for the tester to perform
    # @param expected      the expected verification value
    # @return the final state of the dlg (done, fail, abort), the actual verification value
    def manual_verify(self, parent, title, verify_desc, expected):
        ## see base class for doc
        self._parent = parent
        self._show_dlg_manual_verify(title, verify_desc, expected)
        self._parent.wait_window(self._dlg)
        return self._return_value, self._actual

    # -------------------
    ## show the dlg for performing a manual action
    #
    # @param title   the dlg title
    # @param verify_desc   the action for the tester to perform
    # @param expected      the expected verification value
    # @return None
    def _show_dlg_manual_verify(self, title, verify_desc, expected):
        row = 0
        msg = 'Perform verification, enter Actual, then press Pass or Fail'
        row = self._dlg_common_first(row, title, msg, self._ensure_initials)

        row += 1
        self._create_verify_desc(row, verify_desc)
        services.logger.user(f'verify: {verify_desc}')

        row += 1
        self._create_cell_lbl('Expected:', row, 0)
        row += 1
        self._create_expected(row, expected)
        services.logger.user(f'expected: {expected}')

        row += 1
        self._create_cell_lbl('Actual:', row, 0)
        row += 1
        self._create_actual(row)

        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_pass_btn(row, 0)
        self._create_fail_btn(row, 1)

        ## set callback for handling a click and to ensure intials are set
        self._dlg_common_last(row,
                              self._handle_click,
                              self._ensure_initials)

    # -------------------
    ## the verification action for the tester to perform
    #
    # @param row          the row to place it in
    # @param verify_desc  the verification the tester needs to perform
    # @return None
    def _create_verify_desc(self, row, verify_desc):
        lbl = tkst.ScrolledText(self._frame,
                                wrap=tk.WORD,  # wrap text on a word boundary
                                height=5,  # lines
                                width=self.col0_txt_width,
                                font=self.common_font,
                                fg='black',
                                bg='lightgrey',
                                highlightbackground='black', highlightthickness=2)
        lbl.insert(1.0, verify_desc)
        lbl.configure(state='disabled')  # make it readonly
        lbl.grid(row=row, column=0, sticky='NSWE', columnspan=3)

    # -------------------
    ## the expected value from the verifcation action
    #
    # @param row       the row to place it in
    # @param expected  the expected value of the verification
    # @return None
    def _create_expected(self, row, expected):
        lbl = tkst.ScrolledText(self._frame,
                                wrap=tk.WORD,  # wrap text on a word boundary
                                height=5,  # lines
                                width=self.col0_txt_width,
                                font=self.common_font,
                                fg='black',
                                bg='lightgrey',
                                highlightbackground='black', highlightthickness=2)
        lbl.insert(1.0, expected)
        lbl.configure(state='disabled')  # make it readonly
        lbl.grid(row=row, column=0, sticky='NSWE', columnspan=3)

    # -------------------
    ## btn indicates the tester passed the verification
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_pass_btn(self, row, col):
        self._btn_pass = tk.Button(self._frame, text='Pass',
                                   command=lambda: self._handle_click('pass'),
                                   width=self.col0_btn_width,
                                   font=self.common_font,
                                   fg='black',
                                   bg='lightgreen',
                                   disabledforeground='lightgrey',
                                   highlightbackground='lightgrey', highlightthickness=2)
        self._btn_pass.grid(row=row, column=col, sticky='W')

    # -------------------
    ## disable the Done button
    #
    # @return None
    def _pass_disable(self):
        self._btn_pass['state'] = 'disabled'

    # -------------------
    ## enable the Done button
    #
    # @return None
    def _pass_enable(self):
        self._btn_pass['state'] = 'normal'

    # -------------------
    ## place a highlight around the Done btn
    #
    # @return None
    def _pass_highlight(self):
        self._btn_pass['fg'] = 'black'
        self._btn_pass['highlightbackground'] = 'black'
        self._btn_pass['highlightthickness'] = 2

    # -------------------
    ## unhighlight the Done btn
    #
    # @return None
    def _pass_unhighlight(self):
        self._btn_pass['fg'] = 'black'
        self._btn_pass['highlightbackground'] = 'lightgrey'
        self._btn_pass['highlightthickness'] = 2

    # -------------------
    ## btn that indicates the tester failed the verififcation
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_fail_btn(self, row, col):
        self._btn_fail = tk.Button(self._frame, text='Fail',
                                   command=lambda: self._handle_click('fail'),
                                   width=self.col0_btn_width,
                                   font=self.common_font,
                                   fg='black',
                                   bg='gold',
                                   disabledforeground='lightgrey',
                                   highlightbackground='lightgrey', highlightthickness=2)
        self._btn_fail.grid(row=row, column=col, sticky='W')

    # -------------------
    ## disable the Can't Do button
    #
    # @return None
    def _fail_disable(self):
        self._btn_fail['state'] = 'disabled'

    # -------------------
    ## enable the Can't Do button
    #
    # @return None
    def _fail_enable(self):
        self._btn_fail['state'] = 'normal'

    # -------------------
    ## highlight the Can't Do btn
    #
    # @return None
    def _fail_highlight(self):
        self._btn_fail['fg'] = 'black'
        self._btn_fail['highlightbackground'] = 'black'
        self._btn_fail['highlightthickness'] = 2

    # -------------------
    ## unhighlight the Can't Do button
    #
    # @return None
    def _fail_unhighlight(self):
        self._btn_fail['fg'] = 'black'
        self._btn_fail['highlightbackground'] = 'lightgrey'
        self._btn_fail['highlightthickness'] = 2

    # -------------------
    ## Create the Actual text area. The tester fills
    # it in to indicate the actual value
    #
    # @param row     the row to place it in
    # @return None
    def _create_actual(self, row):
        height = 5
        self._txt_actual = tkst.ScrolledText(self._frame,
                                             wrap=tk.WORD,  # wrap text on a word boundary
                                             height=height,  # lines
                                             width=self.col0_txt_width,
                                             font=self.common_font,
                                             fg='black',
                                             bg='white',
                                             highlightbackground='lightgrey', highlightthickness=2)
        self._txt_actual.configure(state='disabled')  # initially, make it readonly
        self._txt_actual.focus()
        ## set callback for key release
        self._txt_actual.bind('<KeyRelease>', self._actual_key_pressed)
        self._txt_actual.grid(row=row, column=0, sticky='NSWE', columnspan=3)

    # -------------------
    ## handle an entry in the Actual box
    #
    # @param unused   ignored; the key that was pressed
    # @return None
    # noinspection PyUnusedLocal
    def _actual_key_pressed(self, unused):  # pylint: disable=unused-argument
        self._actual_entered = True
        self._get_actual()
        self._check_next()

    # -------------------
    ## get the content form the actual text box
    #
    # @return None
    def _get_actual(self):
        # get the actual text
        self._actual = self._txt_actual.get('1.0', 'end')
        self._actual = self._actual.strip()

    # -------------------
    ## check content of actual field;
    # should be 1 or more characters
    #
    # @return True if _actual has invalid content, False otherwise
    def _actual_is_wrong(self):
        return len(self._actual) < 1

    # -------------------
    ## disable the actual text box
    #
    # @return None
    def _actual_disable(self):
        self._txt_actual['state'] = 'disabled'
        self._txt_actual['fg'] = 'black'

    # -------------------
    ## enable the actual text box
    # note: don't clear out actual text in case the tester wants to extend it
    #
    # @return None
    def _actual_enable(self):
        self._txt_actual['state'] = 'normal'
        self._txt_actual['fg'] = 'black'

    # -------------------
    ## handle a dlg box click
    #
    # @param option  the btn the tester clicked
    # @return None
    def _handle_click(self, option):
        self._get_actual()
        if option == 'pass':
            services.logger.user('click Pass')
            self._actual_enable()
            self._fail_unhighlight()
            self._pass_highlight()
            self._return_value = 'pass'
            self._check_next()

        elif option == 'fail':
            services.logger.user('click Fail')
            self._actual_enable()
            self._fail_highlight()
            self._pass_unhighlight()
            self._return_value = 'fail'
            self._check_next()

        elif option == 'next':
            services.logger.user(f'actual: {self._actual}')
            services.logger.user('click Next')

            ok = self._check_next()
            if ok:
                self._dlg.destroy()

        elif option == 'abort':
            services.logger.user(f'actual: {self._actual}')
            services.logger.user('click Abort')
            self._return_value = 'abort'
            self._dlg.destroy()

    # -------------------
    ## check if Next button should be enabled or not.
    # Set message box as appropriate.
    #
    # @return True if all is ready, False otherwise
    def _check_next(self):
        ok = False
        if self._return_value == 'initial' and not self._actual_entered:
            self._next_disable()
            self._set_message('red', 'Perform verification, enter Actual, then press Pass or Fail')
        elif self._return_value == 'initial' and self._actual_entered:
            # assume that if any value was ever entered in Actual, that the verification was performed
            self._set_message('red', 'Enter Actual, then press Pass or Fail')
        elif self._return_value == 'initial' and not self._actual_is_wrong():
            # actual was entered, but pass or fail wasn't pressed
            self._next_disable()
            self._set_message('red', 'Check Actual, then press Pass or Fail')
        elif self._return_value != 'initial' and self._actual_is_wrong():
            # either Pass or Fail was pressed
            self._next_disable()
            self._set_message('red', 'Actual is too short. Enter Actual value.')
        else:
            # actual is filled in and pass/fail was clicked
            self._next_enable()
            self._set_message('green', f'{self._return_value.capitalize()} selected. '
                                       'Check Actual, press Next when ready')
            ok = True
        return ok

    # -------------------
    ## disable buttons (except abort) if initials box is empty
    #
    # @return None
    def _ensure_initials(self):
        if self._tester_initials_is_wrong():
            self._actual_disable()
            self._pass_disable()
            self._fail_disable()
            self._next_disable()
            self._set_message('red', 'Enter your initials (2 or 3 characters)')
        else:
            self._actual_enable()
            self._pass_enable()
            self._fail_enable()
            self._check_next()
