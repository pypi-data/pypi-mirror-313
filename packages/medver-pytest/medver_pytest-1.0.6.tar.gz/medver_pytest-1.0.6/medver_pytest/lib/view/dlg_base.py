import tkinter as tk

from .. import services
from ..os_specific import OsSpecific


# -------------------
## holds base class for all manual dialog boxes
class DlgBase:  # pylint: disable=too-few-public-methods
    ## constant: width of the dialog box
    width = 850
    ## constant: height of the dialog box
    height = 650
    ## constant: holds font to use for btns and most text and entry widgets
    common_font = ('TkDefaultFont', 13)
    ## constant: holds font to use for smaller areas
    small_font = ('TkDefaultFont', 10, 'bold')
    ## constant: width of the first column for buttons
    col0_btn_width = 11  # characters
    ## constant: width of the first column for text widgets
    col0_txt_width = 14  # characters
    ## constant: width of col 1 and 2
    col12_width = 27

    # -------------------
    ## constructor
    def __init__(self):
        ## main TK window
        self._parent = None

        ## dialog box object
        self._dlg = None
        ## dialog frame
        self._frame = None

        # tester info
        ## the testers name if found in cfg
        self._tester_name = 'unknown'
        ## the tester initials text box
        self._txt_tester_initials = None
        ## the tester name lbl
        self._lbl_tester_name = None

        ## the Next button
        self._btn_next = None

        ## the Message label
        self._lbl_message = None

        ## callback to do additional actions when the initials widget is changed
        self._initials_key_pressed_callback = None

    # -------------------
    ## common first portion of the dlg initialization
    #
    # @param row        the row to use
    # @param msg        the initial message for the msg textbox
    # @param title      the dlg title to use
    # @param fn_ensure_initials  the callback function to use when the initials are set/changed
    # @return last row number
    def _dlg_common_first(self, row, title, msg, fn_ensure_initials):
        services.logger.user(f'display dlg: {title}')
        self._create_dlg(title)

        self._create_message_box(row, msg)

        row += 1

        # disable buttons if initials is empty
        self._initials_key_pressed_callback = fn_ensure_initials

        self._create_tester_info(row)

        return row

    # -------------------
    ## common last portion of the dlg initialization
    #
    # @param row        the row to use
    # @param fn_handle_click     the callback function to use when a click occurs
    # @param fn_ensure_initials  the callback function to use when the initials are set/changed
    # @return None
    def _dlg_common_last(self, row, fn_handle_click, fn_ensure_initials):
        row += 1
        self._create_empty_row(row)

        row += 1
        self._create_next_btn(row, 0, lambda: fn_handle_click('next'))
        self._create_abort_btn(row, 1, lambda: fn_handle_click('abort'))

        row += 1
        self._create_empty_row(row)

        fn_ensure_initials()
        self._set_dlg_location()

    # -------------------
    ## create the TopLevel dialog box
    #
    # @param title   the name of the dlg box
    # @return None
    def _create_dlg(self, title):
        self._dlg = tk.Toplevel(self._parent)

        # temporarily make iconify it (make it invisible)
        self._dlg.withdraw()

        self._dlg.title(title)

        self._dlg.resizable(width=tk.FALSE, height=tk.FALSE)  # remove the max window button
        ## set callback for Delete Window
        self._dlg.protocol('WM_DELETE_WINDOW', self._disable_event)

        self._dlg.config(bg='lightgrey')
        self._create_frame()

    # -------------------
    ## set the dlg location based on the last position saved, if any.
    # otherwise center the dlg in the current screen
    #
    # @return None
    def _set_dlg_location(self):
        # dlgbox is created, but all content may not be updated yet
        self._parent.update_idletasks()
        self._dlg.update_idletasks()

        # show the window
        self._dlg.deiconify()

        # use last position if non-0, otherwise center it
        if services.status.last_position_saved():
            OsSpecific.init()
            if OsSpecific.os_name == 'macos':
                offset = 0
            else:
                # note: the 37 is the height of the OS provided top bar
                offset = 37
            self._dlg.geometry(f'+{services.status.last_position_x}+{services.status.last_position_y - offset}')
            self._dlg.update_idletasks()
        else:
            # center the window
            self._parent.eval(f'tk::PlaceWindow {str(self._dlg)} center')
            self._dlg.update_idletasks()
            services.status.save_last_position(self._dlg.winfo_x(), self._dlg.winfo_y())

        ## set callback for Configure
        self._dlg.bind('<Configure>', self._on_move)

    # -------------------
    ## callback when the dlg is moved
    #
    # @param event   the tkinter config event that occurred
    # @return None
    def _on_move(self, event):  # pylint: disable=unused-argument
        # note: this will get events for all children within the dlg box

        # uncomment to debug
        # services.logger.dbg(f'move: {self._dlg.winfo_x()}, {self._dlg.winfo_y()}')

        # save the dlg box frame x,y
        services.status.save_last_position(self._dlg.winfo_x(), self._dlg.winfo_y())

    # -------------------
    ## used to ignore click events
    #
    # @return None
    def _disable_event(self):
        pass

    # -------------------
    ## create the Frame that holds the grid of buttons, text, etc.
    #
    # @return None
    def _create_frame(self):
        self._frame = tk.Frame(self._dlg,
                               bg='lightgrey')
        self._frame.pack(padx=1, pady=5)
        self._frame.grid_columnconfigure(0, weight=1)

    # -------------------
    ## create the tester information: initials and name.
    # the name is retried from the cfg file based on the given initials.
    # there can be 2 or 3 initials only
    #
    # @param row   the row to place these widgets in
    # @return None
    def _create_tester_info(self, row):
        self._create_tester_initials(row, 0)
        self._create_tester_name(row, 1)

    # -------------------
    ## create the tester initials Entry box
    #
    # @param row   the row to place the widget in
    # @param col   the column to place the widget in
    # @return None
    def _create_tester_initials(self, row, col):
        self._txt_tester_initials = tk.Entry(self._frame,
                                             width=self.col0_txt_width,
                                             font=self.common_font,
                                             bg='lightgrey',
                                             fg='black',
                                             highlightbackground='black', highlightthickness=1
                                             )
        services.logger.user(f'tester initials: "{services.status.last_tester_initials}"')
        self._txt_tester_initials.insert(0, services.status.last_tester_initials)
        self._txt_tester_initials.focus()
        ## set callback for KeyRelease
        self._txt_tester_initials.bind('<KeyRelease>', self._initials_key_pressed)
        self._txt_tester_initials.grid(row=row, column=col, sticky='W')

    # -------------------
    ## indicates if the tester initials has 2 or 3 characters
    #
    # @return True if 2 or 3 chars, False otherwise
    def _tester_initials_is_wrong(self):
        num = len(services.status.last_tester_initials)
        return num < 2 or num > 3

    # -------------------
    ## create tester name label. Filled based on tester initials and content of cfg file
    #
    # @param row  the row to place it in
    # @param col  the column to place it in
    # @return None
    def _create_tester_name(self, row, col):
        self._get_tester_name()
        self._lbl_tester_name = tk.Label(self._frame,
                                         text=self._tester_name,
                                         anchor='w',
                                         width=self.col12_width,
                                         height=1,
                                         font=self.common_font,
                                         fg='black',
                                         bg='lightgrey')
        self._lbl_tester_name.grid(row=row, column=col, sticky='NEWS', columnspan=2, ipady=5)

    # -------------------
    ## handle an entry in the tester initial box
    #
    # @param unused   ignored; the key that was pressed
    # @return None
    # noinspection PyUnusedLocal
    def _initials_key_pressed(self, unused):  # pylint: disable=unused-argument
        services.status.last_tester_initials = self._txt_tester_initials.get().upper().strip()
        self._get_tester_name()
        self._lbl_tester_name.config(text=self._tester_name,
                                     fg='black', bg='white',
                                     width=self.col12_width)

        if self._initials_key_pressed_callback:
            self._initials_key_pressed_callback()  # pylint: disable=not-callable

    # -------------------
    ## translate tester initials into tester name
    #
    # @return None
    def _get_tester_name(self):
        if services.status.last_tester_initials in services.cfg.testers:
            self._tester_name = services.cfg.testers[services.status.last_tester_initials]
        else:
            self._tester_name = 'unknown'
        services.logger.user(f'tester name: "{self._tester_name}"')

    # -------------------
    ## create empty row
    #
    # @param row  the row to place it in
    # @return None
    def _create_empty_row(self, row):
        lbl = tk.Label(self._frame, text=' ',
                       width=0,
                       font=self.common_font,
                       fg='lightgrey',
                       bg='lightgrey',
                       highlightbackground='lightgrey', highlightthickness=1)
        lbl.configure(state='disabled')  # make it readonly
        lbl.grid(row=row, column=0, sticky='W')

    # -------------------
    ## crate a label widget
    #
    # @param text    the text for the widget
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @param height  the height (in lines) of the lbl widget
    # @return None
    def _create_cell_lbl(self, text, row, col, height=1):
        lbl = tk.Label(self._frame,
                       text=text,
                       anchor='sw',
                       height=height,
                       width=self.col0_txt_width,
                       font=self.small_font,
                       fg='black',
                       bg='lightgrey')
        lbl.grid(row=row, column=col, sticky='EWS', pady=(5, 0), ipady=2)

    # -------------------
    ## btn that indicates the tester wants to abort the test
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @param fn_handle_click  the callback for handling a click
    # @return None
    def _create_abort_btn(self, row, col, fn_handle_click):
        btn = tk.Button(self._frame, text='Abort', command=fn_handle_click,
                        font=self.common_font,
                        fg='black',
                        bg='red',
                        width=self.col0_btn_width)
        btn.grid(row=row, column=col, sticky='W')

    # -------------------
    ## Create the Next btn. The tester presses
    # it to go to the next protocol step.
    #
    # @param row     the row to place it in
    # @param col     the column to place it in
    # @param fn_handle_click  the callback for handling a click
    # @return None
    def _create_next_btn(self, row, col, fn_handle_click):
        # initially disabled
        self._btn_next = tk.Button(self._frame, text='Next', command=fn_handle_click,
                                   state='disabled',
                                   font=self.common_font,
                                   fg='black',
                                   bg='darkblue',
                                   disabledforeground='lightgrey',
                                   width=self.col0_btn_width)
        self._btn_next.grid(row=row, column=col, sticky='W')

    # -------------------
    ## enable the Next btn
    #
    # @return None
    def _next_enable(self):
        self._btn_next['state'] = 'normal'

    # -------------------
    ## disable the Next btn
    #
    # @return None
    def _next_disable(self):
        self._btn_next['state'] = 'disabled'

    # -------------------
    ## create message box label. Filled with messages to the tester
    #
    # @param row  the row to place it in
    # @param msg  the message to display
    # @return None
    def _create_message_box(self, row, msg):
        self._lbl_message = tk.Label(self._frame,
                                     text=msg,
                                     anchor='center',
                                     wraplength=self.width,
                                     font=self.small_font,
                                     fg='black',
                                     bg='lightgrey',
                                     highlightbackground='black', highlightthickness=1)
        self._set_message('black', 'Press Can\'t do or perform the action and press Done')
        self._lbl_message.grid(row=row, column=0, sticky='NEW', columnspan=3, pady=(0, 5), ipady=10)

    # -------------------
    ## set the text of the message box
    #
    ## @param color  the color to print the text in
    ## @param text   the text to display
    # @return None
    def _set_message(self, color, text):
        self._lbl_message.config(text=text, fg=color)
