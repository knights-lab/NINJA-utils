import subprocess
import os


def run_command(cmd, shell=False):
    """
    Run prepared behave command in shell and return its output.
    :param cmd: Well-formed behave command to run.
    :param shell: Force subprocess to use shell, not recommended
    :return: Command output as string.
    """

    try:
        output = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=shell,
            cwd=os.getcwd(),
        )

    except subprocess.CalledProcessError as e:
        output = e.output

    return output
