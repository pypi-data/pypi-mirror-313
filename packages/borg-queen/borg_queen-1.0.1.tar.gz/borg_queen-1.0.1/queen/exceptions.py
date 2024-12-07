class QueenException(Exception):
    pass


class QueenSubprocessException(QueenException):
    def __init__(self, args, code, stderr=""):
        self.args = args
        self.code = code
        self.stderr = stderr

        message = "'%s' failed with error code %s." % (
            " ".join(args),
            code,
        )

        if stderr:
            message = "%s stderr: %s" % (message, stderr)

        super().__init__(message)
