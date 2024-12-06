import sys


# -------------------
## Holds all info for logging debug lines
class Logger:
    ## flag to log to stdout or not
    verbose = True
    ## for UT only
    ut_mode = False
    ## for UT only
    ut_lines = []

    # --------------------
    ## log a message. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param msg     the message to print
    # @return None
    @staticmethod
    def check(ok, msg):
        if ok:
            Logger.ok(msg)
        else:
            Logger.err(msg)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param msgs    individual list of lines to print
    # @return None
    @staticmethod
    def check_all(ok, title, msgs):
        Logger.check(ok, f'{title}: {ok}')
        for msg in msgs:
            Logger.check(ok, f'   - {msg}')

    # -------------------
    ## write a "====" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def start(msg):
        Logger._write_line('====', msg)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def line(msg):
        Logger._write_line(' ', msg)

    # -------------------
    ## write a "highlight" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def highlight(msg):
        Logger._write_line('--->', msg)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def ok(msg):
        Logger._write_line('OK', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def err(msg):
        Logger._write_line('ERR', msg, always_print=True)

    # -------------------
    ## write a "bug" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def bug(msg):
        Logger._write_line('BUG', msg, always_print=True)

    # -------------------
    ## write an output line with the given message
    #
    # @param msg     the message to write
    # @param lineno  (optional) the current line number for each line printed
    # @return None
    @staticmethod
    def output(msg, lineno=None):
        if lineno is None:
            tag = ' --    '
        else:
            tag = f' --{lineno: >3}]'
        Logger._write_line(tag, msg)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def warn(msg):
        Logger._write_line('WARN', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def dbg(msg):
        Logger._write_line('DBG', msg)

    # -------------------
    ## write a raw line (no tag) with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def raw(msg):
        Logger._write_line(None, msg)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag           the prefix tag
    # @param msg           the message to write
    # @param always_print  print the message even if verbose is False
    # @return None
    @staticmethod
    def _write_line(tag, msg, always_print=False):
        if not Logger.verbose and not always_print:
            return

        # TODO add ability to optionally save to file

        if tag is None:
            line = msg
        else:
            line = f'{tag: <4} {msg}'

        if Logger.ut_mode:
            Logger.ut_lines.append(line)
        else:
            print(line)  # print okay
            sys.stdout.flush()
