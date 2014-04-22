import sys
import os
import time
import traceback
from proflib.lib.docstrings import get_code_of_function

class FrameStackTrace(object):
    """
    Encapsulates the Code of a function
    """

    def __init__(self, frame):
        self.frame = frame
        self.stack_trace = traceback.format_stack()

    """ GETTERS """
    @property
    def stack_trace(self):
        """
        Return the raw stack trace
        """
        return self._stack_trace

    @property
    def frame(self):
        """
        Return the frame associated with this code
        """
        return self._frame

    """ SETTERS """
    @stack_trace.setter
    def stack_trace(self, value):
        """
        Set the raw stack trace
        """
        self._stack_trace = value

    @frame.setter
    def frame(self, value):
        """
        Set the frame associated with this code
        """
        self._frame = value
