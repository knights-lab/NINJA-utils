import os
import sys

from .path import verify_make_dir


class Logger:
    """
        A convenient logging object
        Prints output to a given log file and/or stdout
    """

    def __init__(self, logfp=None, use_std_out=True):
        # note: if logfp directories don't exist, make them.

        if logfp is not None:
            outdir = os.path.abspath(os.path.dirname(os.path.realpath(logfp)))

            # Checks for output directory. Makes it if necessary.
            verify_make_dir(outdir)

        self.logfp = logfp
        log_file = open(logfp, 'w')
        log_file.close()
        self.use_std_out = use_std_out

    def log(self, msg):
        if not msg.endswith('\n'):
            msg += '\n'
        if self.logfp is not None:
            log_file = open(self.logfp, 'a')
            log_file.write(msg)
            log_file.close()
        if self.use_std_out:
            sys.stdout.write(msg)
