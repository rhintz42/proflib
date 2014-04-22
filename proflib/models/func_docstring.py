import sys
import os
import time
import traceback
from proflib.lib.docstrings import get_docstring_of_function

class FuncDocstring(object):
    """
    Encapsulates the Docstring of a function
    """

    def __init__(self, function_details):
        self.function_details = function_details
        self.docstring = get_docstring_of_function( function_details.file_path,
                                                    function_details.function_name )

    """ GETTERS """
    @property
    def docstring(self):
        """
        Return the raw docstring
        """
        return self._docstring

    @property
    def function_details(self):
        """
        Return the function_details associated with this docstring
        """
        return self._function_details

    """ SETTERS """
    @docstring.setter
    def docstring(self, value):
        """
        Set the raw docstring
        """
        self._docstring = value

    @function_details.setter
    def function_details(self, value):
        """
        Set the function_details associated with this docstring
        """
        self._function_details = value
