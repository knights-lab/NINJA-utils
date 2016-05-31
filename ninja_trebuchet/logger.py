import os
import sys
import time

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
        if not msg.endswith(os.linesep):
            msg += os.linesep
        if self.logfp is not None:
            log_file = open(self.logfp, 'a')
            log_file.write('[%s] %s' % (time.strftime("%x %X", time.localtime()), msg))
            log_file.close()
        elif self.use_std_out:
            sys.stdout.write(msg)
