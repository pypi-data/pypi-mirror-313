from subprocess import PIPE, Popen

from .exceptions import QueenSubprocessException


def launch(args, **kwargs):
    """Launch a subprocess, wait for it to finish and return its return code
    and stderr.
    """
    kwargs.update(
        {
            "stderr": PIPE,
            "universal_newlines": True,  # force text mode on stderr pipe
        }
    )
    p = Popen(args, **kwargs)

    _, stderr = p.communicate()
    return p.returncode, stderr


def run(args, **kwargs):
    """Launch a subprocess and raise an exception if it fails"""
    code, stderr = launch(args, **kwargs)

    if code != 0:
        raise QueenSubprocessException(args, code, stderr)


def run_interactive(args, **kwargs):
    """Launch a subprocess and interactively print its stderr

    It contains a bunch of special cases that don't apply generally, but handle
    specifically "borg creteate --progress ..." output.
    """
    kwargs.update(
        {
            "stderr": PIPE,
            "universal_newlines": True,  # force text mode on stderr pipe
            "bufsize": 1,
        }
    )
    p = Popen(args, **kwargs)

    # It's much easier to read the process' stderr as text, strip the newlines
    # that python added and add a \r to emulate borg's display.
    # A proper solution would be to read stderr as binary and handle everything
    # else ourselves.
    for line in p.stderr:
        s = "%s\r" % line.rstrip("\n")
        print(s, end="")

    p.wait()

    if p.returncode != 0:
        raise QueenSubprocessException(args, p.returncode)
