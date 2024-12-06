import sys


# -------------------
## Holds all info for logging debug lines
class UtilsLogger:
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
            UtilsLogger.ok(msg)
        else:
            UtilsLogger.err(msg)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param msgs    individual list of lines to print
    # @return None
    @staticmethod
    def check_all(ok, title, msgs):
        UtilsLogger.check(ok, f'{title}: {ok}')
        for msg in msgs:
            UtilsLogger.check(ok, f'   - {msg}')

    # -------------------
    ## write a "====" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def start(msg):
        UtilsLogger._write_line('====', msg)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def line(msg):
        UtilsLogger._write_line(' ', msg)

    # -------------------
    ## write a "highlight" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def highlight(msg):
        UtilsLogger._write_line('--->', msg)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def ok(msg):
        UtilsLogger._write_line('OK', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def err(msg):
        UtilsLogger._write_line('ERR', msg, always_print=True)

    # -------------------
    ## write a "bug" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def bug(msg):
        UtilsLogger._write_line('BUG', msg, always_print=True)

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
        UtilsLogger._write_line(tag, msg)

    # -------------------
    ## write a list of lines using output()
    #
    # @param lines   the lines to write
    # @return None
    @staticmethod
    def num_output(lines):
        lineno = 0
        for line in lines:
            lineno += 1
            UtilsLogger.output(line, lineno=lineno)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def warn(msg):
        UtilsLogger._write_line('WARN', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def dbg(msg):
        UtilsLogger._write_line('DBG', msg)

    # -------------------
    ## write a raw line (no tag) with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def raw(msg):
        UtilsLogger._write_line(None, msg)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag           the prefix tag
    # @param msg           the message to write
    # @param always_print  print the message even if verbose is False
    # @return None
    @staticmethod
    def _write_line(tag, msg, always_print=False):
        if not UtilsLogger.verbose and not always_print:
            return

        # TODO add ability to optionally save to file

        if tag is None:
            line = msg
        else:
            line = f'{tag: <4} {msg}'

        if UtilsLogger.ut_mode:
            UtilsLogger.ut_lines.append(line)
        else:
            print(line)  # print okay
            sys.stdout.flush()
