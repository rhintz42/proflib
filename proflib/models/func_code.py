import sys
import os
import time
import traceback
from proflib.lib.filelib import get_function_code

class FuncCode(object):
    """
    Encapsulates the Code of a function
    """

    def __init__(self, function_details):
        self.function_details = function_details
        self.code = get_function_code( function_details.file_path,
                                       function_details.function_name )


    """ GETTERS """
    @property
    def code(self):
        """
        Return the raw code
        """
        return self._code

    @property
    def function_details(self):
        """
        Return the function_details associated with this code
        """
        return self._function_details

    """ SETTERS """
    @code.setter
    def code(self, value):
        """
        Set the raw code
        """
        self._code = value

    @function_details.setter
    def function_details(self, value):
        """
        Set the function_details associated with this code
        """
        self._function_details = value
