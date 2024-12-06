# The goal here is to add multiple, simultaneous progress bars.
# TODO: handle concurrent groups and bars finishing
# TODO: handle messages that are too long
# TODO: handle terminals without escape sequences (single line for all bars)

class progress:
    """
    Provide an object to store the state of a progress bar and methods to create
    and update the progress bar in the terminal.

    Attributes
    ----------
    J_bars : int
        Number of active progress bars.

    Notes
    -----
    To create a progress bar write

        bar = Progress(K)

    Here, `K` is the reference value for the progress bar. In other words, if
    there is a counter `k`, the assumption is that the counter has a minimum
    value of 0 a maximum value of `K`. This way, you do not need to pass the
    ratio `k/K` every time the progress bar is updated. The progress bar will
    look like this:

        14% =====---------------------------  00:00:11.7

    On the left is the percentage of the progress. On the right is the total
    elapsed time in hours, minutes, and seconds. In the middle is the visual
    representation of the progress bar showing ticks filling up the empty space
    between the brackets. The total width of this display is 60 characters, by
    default. But, the user can change this by defining `cols` when creating a
    new progress bar:

        bar = Progress(K, cols=50)

    You cannot set `cols` to less than 30. The user can also specify a message
    to display to the right of a progress bar by defining the `msg` parameter:

        bar = Progress(K, msg='Writing file ...', cols=50)

    The message text does not count towards the overall width of the progress
    bar. With the message, we get something like this:

        14%  =====---------------------------  00:00:11.7  Writing file ...

    To update the progress bar and refresh its display in the terminal, call the
    `update` method on the progress bar object:

        bar.update(k)

    You can also change the message for the progress bar when you call the
    `update` method by defining the `msg` parameter.

    You can call the update method as often as you like; however, it will only
    print if either at least 1/10 of a second has passed or the value passed
    equals the reference value or the message has changed. This helps to
    significantly reduce the computational burden of calling the `update`
    method. The overwhelming majority of the computational burden comes from
    actually printing to the screen. So, feel free to call the `update` method
    more often than every 1/10 of a second. In testing, this implementation was
    actually more efficient than the tqdm library.

    You can run multiple progress bars simultaneously. Each progress bar will be
    displayed on its own line in the terminal, if `terminal` is set to `True`.
    You can also reuse progress bars. If the value of a progress bar has
    previously reached ref_value but now is less than ref_value, the progress
    bar will automatically reset. This will reset the starting time to the last
    time the `update` method was called.

    For consoles which do not support moving the cursor up or down (e.g.,
    Jupyter Notebooks), set the `terminal` parameter to False. Then, all the
    bars will print on the same line. You might have a problem if all the bars
    cannot fit onto one line. At that point, you will get bars printed onto new
    lines each call to the `update` method.
    """

    # Counter for the total number of progress bars in play.
    J_bars = 0

    def __init__(self, K=1, cols=1, uni=None, msg=None):
        """
        Initialize a new progress bar object.

        Parameters
        ----------
        K : int, default 1
            Final value of counter k, plus 1.
        cols : int or float, default 1
            Desired width of the full string, including the percent complete,
            the bar, and the clock if greater than 1 or fraction of window
            columns if less than 1.
        uni : bool, default None
            Flag to use Unicode characters for plotting. This overrides the
            value defined in config.ini.
        msg : string, default None
            Message string to print to the right of the bar.

        Attributes
        ----------
        K : int
            Final value of counter k, plus 1.
        t_init : float
            Time of initialization of the progress bar object.
        t_last : float
            Time of last progress bar print.
        msg : string, default None
            Message string to print to the right of the bar.
        use_esc : bool
            Flag to use ANSI escape sequences. This only matters when the plot
            function runs in a limited terminal.
        bar_width : int
            Columns dedicated to the actual bar of the progress bar.
        uni : bool, default None
            Flag to use Unicode characters for plotting. This overrides the
            value defined in config.ini.
        done : bool
            Flag to determine if a progress bar is finished.
        j_bar : int
            Index of current progress bar.
        """

        # Get lengths of percent and clock strings:
        len_percent = len("100% ")
        len_clock = len(" -99:59:59.9")

        # Save the input settings.
        self.K = max(K, 1)
        self.t_init = time.perf_counter()
        self.t_last = self.t_init
        self.msg = msg

        # Get the terminal size.
        term_cols, _ = term_size()
        self.use_esc = is_term()

        # Convert a fractional cols to columns.
        if cols <= 1:
            cols = round(term_cols * cols)
            cols = max(cols, 1 + len_percent + len_clock)
        else:
            cols = min(max(cols, 1 + len_percent + len_clock), term_cols)

        # Define the bar width.
        self.bar_width = cols - len_percent - len_clock

        # Decide whether to use Unicode characters.
        if (uni is None) or not isinstance(uni, bool):
            uni = Config.uni
        self.uni = uni

        # Initialize the done flag, which marks if k has reached K - 1.
        self.done = False

        # The `j_bar` is used to keep track of which row of text a progress bar
        # is on relative to the current row of text.
        self.j_bar = progress.J_bars
        progress.J_bars += 1

        # Print the initial string.
        draw_str = HIDE_CURSOR if self.use_esc else ""
        draw_str += "  0% "
        draw_str += fill_bar(0.0, self.bar_width, self.use_esc, True, self.uni)
        if self.use_esc:
            draw_str += RESET
        draw_str += "  ##:##:##.#"
        if self.msg is not None:
            draw_str += f"  {self.msg}"
        if self.use_esc:
            draw_str += SHOW_CURSOR

        # Add cursor motions. Up: "\x1b[1A". Down: "\x1b[1B". Beginning of row:
        # "\x1b[G". Clear row: "\x1b[2K". Print a new line, so the rest state is
        # a row of text below all the progress bars.
        if self.use_esc:
            draw_str = "\n\x1b[1A\x1b[2K" + draw_str + "\x1b[1B\x1b[G"

        # Print the full string. Do not return at the end of the printed string.
        # The return is already built into the string commands.
        sys.stdout.write(draw_str)
        sys.stdout.flush()

    def update(self, k, msg=None):
        """
        Update the progress bar object.

        Parameters
        ----------
        k : float or int
            The progress counter. This should be an integer between 0 and K - 1.
        msg : string, default None
            Any new message string.
        """

        # Get the elapsed time.
        t_now = time.perf_counter()

        # If the value is not the reference value, less than 1/10 of a second
        # has past, and the message has not changed, return from this method.
        if (k < self.K - 1) and (abs(t_now - self.t_last) < 0.1) \
                and ((msg is None) or (msg == self.msg)):
            return

        # Convert k to ratio. Ensure k is between 0 and K - 1.
        k = min(max(int(k), 0), self.K - 1)
        ratio = k/(self.K - 1)

        # Check if a reset is needed or if the timer should be stopped.
        if self.done: # If it is stopped,
            if k < self.K - 1: # but k dropped, then reset.
                self.t_init = self.t_last + 0
                self.done = False
        elif k == self.K - 1: # If was not done, but is now,
            self.done = True
        self.t_last = t_now

        # Check if the message should be updated.
        if msg is not None:
            self.msg = msg

        # Build the clock string.
        t_show = t_now - self.t_init
        if k == self.K - 1:
            clk_str = "  "
        else:
            t_show = 0.0 if ratio <= 0 else t_show*(1 - ratio)/ratio
            clk_str = " -"
        hours = int(t_show/3600)
        minutes = int((t_show - hours*3600)//60)
        seconds = t_show % 60
        clk_str += f"{hours:02d}:{minutes:02d}:{seconds:04.1f}"

        # Assemble the full string.
        draw_str = HIDE_CURSOR if self.use_esc else ""
        draw_str += f"{int(100*ratio):3d}% "
        draw_str += fill_bar(self.bar_width*ratio, self.bar_width,
                self.use_esc, True, self.uni)
        if self.use_esc:
            draw_str += RESET
        draw_str += f"{clk_str}"
        if self.msg is not None:
            draw_str += "  %s" % (self.msg)
        if self.use_esc:
            draw_str += SHOW_CURSOR

        # Add cursor motions. Up: "\x1b[1A". Down: "\x1b[1B". Beginning of row:
        # "\x1b[G". Clear row: "\x1b[2K". Print a new line, so the rest state is
        # a row of text below all the progress bars.
        rows_offset = progress.J_bars - self.j_bar
        if self.use_esc:
            draw_str = "\x1b[%dA\x1b[G\x1b[2K" % (rows_offset) + \
                    draw_str + "\x1b[%dB\x1b[G" % (rows_offset)
        else:
            draw_str = "\r" + draw_str

        # Print the full string. Do not return at the end of the printed string.
        # The return is already built into the string commands.
        sys.stdout.write(draw_str)
        sys.stdout.flush()
