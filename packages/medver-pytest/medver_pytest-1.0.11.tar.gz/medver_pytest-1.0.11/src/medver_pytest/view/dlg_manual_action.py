import tkinter as tk
import tkinter.scrolledtext as tkst

from .dlg_base import DlgBase
from .. import services


# -------------------
## holds Dialog Box for a Manual Action Step
class DlgManualAction(DlgBase):
    # -------------------
    ## constructor
    def __init__(self):
        ## see base class for doc
        self._dlg = None

        ## see base class for doc
        self._dlg = None
        super().__init__()

        ## the return state, holds abort, done, or cantdo
        self._return_value = 'initial'
        ## the reason text if state is cantdo, otherwise ''
        self._reason = ''
        ## whether reason was entered or not
        self._reason_entered = False

        # widgets
        ## the Done btn
        self._btn_done = None
        ## the Can't do btn
        self._btn_cantdo = None
        ## the Reason Text widget
        self._txt_reason = None

    # -------------------
    ## show dialog for a manual action
    #
    # @param parent   the tk root window
    # @param title    the dlg title
    # @param action   the action for the tester to perform
    # @return the final state of the dlg (done, cantdo, abort), the reason if state is cantdo, otherwise ''
    def step_manual_action(self, parent, title, action):
        ## see base class for doc
        self._parent = parent
        self._show_dlg_manual_action(title, action)
        self._parent.wait_window(self._dlg)

        return self._return_value, self._reason

    # -------------------
    ## show the dlg for performing a manual action
    #
    # @param title   the dlg title
    # @param action  the action for the tester to perform
    # @return None
    def _show_dlg_manual_action(self, title, action):
        row = 0
        msg = 'Press Can\'t do or perform the action and press Done'
        row = self._dlg_common_first(row, title, msg, self._ensure_initials)

        row += 1
        self._create_action_desc(row, action)
        services.logger.user(f'action: {action}')

        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_done_btn(row)

        row += 1
        self._create_cantdo_btn(row, 0)

        row += 1
        self._create_cell_lbl('Reason cannot be done:', row, 0)
        row += 1
        self._create_reason(row, 0)

        ## set callbacks for click and ensure initials
        self._dlg_common_last(row,
                              self._handle_click,
                              self._ensure_initials)

    # -------------------
    ## the action for the tester to perform
    #
    # @param row          the row to place it in
    # @param action_desc  the tester action needed for the current protocol step
    # @return None
    def _create_action_desc(self, row, action_desc):
        lbl = tkst.ScrolledText(self._frame,
                                wrap=tk.WORD,  # wrap text on a word boundary
                                height=5,  # lines
                                width=self.col0_txt_width,
                                font=self.common_font,
                                fg='black',
                                bg='lightgrey',
                                highlightbackground='black', highlightthickness=2)
        lbl.insert(1.0, action_desc)
        lbl.configure(state='disabled')  # make it readonly
        lbl.grid(row=row, column=0, sticky='WE', columnspan=3)

    # -------------------
    ## btn indicates action was done
    #
    # @param row     the row to place it in
    # @return None
    def _create_done_btn(self, row):
        self._btn_done = tk.Button(self._frame, text='Done',
                                   command=lambda: self._handle_click('done'),
                                   width=self.col0_btn_width,
                                   font=self.common_font,
                                   fg='black',
                                   bg='lightgreen',
                                   disabledforeground='lightgrey',
                                   highlightbackground='black', highlightthickness=2)
        self._btn_done.grid(row=row, column=0, sticky='W')

    # -------------------
    ## disable the Done button
    #
    # @return None
    def _done_disable(self):
        self._btn_done.config(state='disabled', fg='black', highlightbackground='black', highlightthickness=0)

    # -------------------
    ## enable the Done button
    #
    # @return None
    def _done_enable(self):
        self._btn_done.config(state='normal', fg='black', highlightbackground='black', highlightthickness=2)

    # -------------------
    ## place a highlight around the Done btn
    #
    # @return None
    def _done_highlight(self):
        self._btn_done.config(fg='black', highlightbackground='black', highlightthickness=2)

    # -------------------
    ## unhighlight the Done btn
    #
    # @return None
    def _done_unhighlight(self):
        self._btn_done.config(fg='black', highlightbackground='lightgrey', highlightthickness=2)

    # -------------------
    ## btn that indicates the tester can't do the requested action
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_cantdo_btn(self, row, col):
        self._btn_cantdo = tk.Button(self._frame, text='Can\'t Do',
                                     command=lambda: self._handle_click('cantdo'),
                                     width=self.col0_btn_width,
                                     font=self.common_font,
                                     fg='black',
                                     bg='gold',
                                     disabledforeground='lightgrey',
                                     highlightbackground='black', highlightthickness=2)
        self._btn_cantdo.grid(row=row, column=col, sticky='W')

    # -------------------
    ## disable the Can't Do button
    #
    # @return None
    def _cantdo_disable(self):
        self._btn_cantdo.config(state='disabled', fg='black', highlightbackground='black', highlightthickness=0)

    # -------------------
    ## enable the Can't Do button
    #
    # @return None
    def _cantdo_enable(self):
        self._btn_cantdo.config(state='normal', fg='black', highlightbackground='black', highlightthickness=2)

    # -------------------
    ## highlight the Can't Do btn
    #
    # @return None
    def _cantdo_highlight(self):
        self._btn_cantdo.config(fg='black', highlightbackground='black', highlightthickness=2)

    # -------------------
    ## unhighlight the Can't Do button
    #
    # @return None
    def _cantdo_unhighlight(self):
        self._btn_cantdo.config(fg='black', highlightbackground='lightgrey', highlightthickness=2)

    # -------------------
    ## Create the Reason text area. The tester fills
    # it in if they can not perform the requested action
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @return None
    def _create_reason(self, row, col):
        self._txt_reason = tkst.ScrolledText(self._frame,
                                             wrap=tk.WORD,  # wrap text on a word boundary
                                             height=5,  # lines
                                             width=self.col12_width,
                                             font=self.common_font,
                                             fg='black',
                                             bg='lightgrey',
                                             highlightbackground='black', highlightthickness=2)
        self._txt_reason.configure(state='disabled')  # initially, make it readonly
        self._txt_reason.focus()
        ## set callback for key release
        self._txt_reason.bind('<KeyRelease>', self._reason_key_pressed)
        self._txt_reason.grid(row=row, column=col, sticky='NEWS', columnspan=3)

    # -------------------
    ## handle an entry in the Reason box
    #
    # @param unused   ignored; the key that was pressed
    # @return None
    # noinspection PyUnusedLocal
    def _reason_key_pressed(self, unused):  # pylint: disable=unused-argument
        self._reason_entered = True
        self._get_reason()
        self._check_next()

    # -------------------
    ## get the content form the reason text box
    #
    # @return None
    def _get_reason(self):
        # get the reason text
        self._reason = self._txt_reason.get('1.0', 'end')
        self._reason = self._reason.strip()

    # -------------------
    ## check content of reason field;
    # should be 2 or more characters
    #
    # @return True if _reason has invalid content, False otherwise
    def _reason_is_wrong(self):
        return len(self._reason) < 2

    # -------------------
    ## disable the Reason text box
    #
    # @return None
    def _reason_disable(self):
        self._txt_reason['state'] = 'disabled'
        self._txt_reason['fg'] = 'darkgrey'
        self._txt_reason['bg'] = 'lightgrey'

    # -------------------
    ## enable the Reason text box
    # note: don't clear out reason text in case the tester wants to extend it
    #
    # @return None
    def _reason_enable(self):
        self._txt_reason['state'] = 'normal'
        self._txt_reason['fg'] = 'black'
        self._txt_reason['bg'] = 'white'

    # -------------------
    ## handle a dlg box click
    #
    # @param option  the btn the tester clicked
    # @return None
    def _handle_click(self, option):
        self._get_reason()
        if option == 'done':
            services.logger.user('click Done')
            self._reason_disable()
            self._cantdo_unhighlight()
            self._done_highlight()
            self._return_value = 'done'
            self._check_next()

        elif option == 'cantdo':
            services.logger.user('click Can\t Do')
            self._reason_enable()
            self._cantdo_highlight()
            self._done_unhighlight()
            self._return_value = 'cantdo'
            self._check_next()

        elif option == 'next':
            services.logger.user(f'reason: {self._reason}')
            services.logger.user('click Next')

            ok = self._check_next()
            if ok:
                self._dlg.destroy()

        elif option == 'abort':
            services.logger.user(f'reason: {self._reason}')
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
        if self._return_value == 'initial' and not self._reason_entered:
            self._next_disable()
            self._set_message('red', 'Perform step action, then Press Done or Press Can\'t Do')
        elif self._return_value == 'initial' and self._reason_entered:
            self._next_disable()
            # assume that if a value was entered in Reason, the action can't be done
            self._set_message('red', 'Check Reason, press Can\'t Do, and then press Next')
        elif self._return_value == 'cantdo' and self._reason_is_wrong():
            self._next_disable()
            self._set_message('red', 'Reason is too short. Enter full Reason.')
        elif self._return_value == 'cantdo' and not self._reason_is_wrong():
            self._next_enable()
            self._set_message('green', 'Can\'t Do selected. Check Reason, press Next when ready')
            ok = True
        elif self._return_value == 'done':
            self._next_enable()
            self._set_message('green', 'Done selected. Press Next when ready')
            ok = True
        else:
            services.logger.err(f'dlg_manual_action._check_next: invalid combination: {self._return_value} '
                                f'reason_entered:{self._reason_entered} '
                                f'reason_is_wrong:{self._reason_is_wrong()}')
            # TODO abort?
        return ok

    # -------------------
    ## disable buttons (except abort) if initials box is empty
    #
    # @return None
    def _ensure_initials(self):
        if self._tester_initials_is_wrong():
            self._reason_disable()
            self._done_disable()
            self._cantdo_disable()
            self._next_disable()
            self._set_message('red', 'Enter your initials (2 or 3 characters)')
        else:
            self._done_enable()
            self._cantdo_enable()
            self._check_next()
