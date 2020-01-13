class PyJenaUtilsException(Exception):
    def __init__(self, orig_exception, message):
        self.orig_exception = orig_exception
        self.message = message
