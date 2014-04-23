import sys
import os
import time
import traceback
from proflib.lib.filelib import get_docstring_of_function, \
                                   get_code_of_function
from proflib.models.func_code import FuncCode
from proflib.models.func_docstring import FuncDocstring

class FunctionDetails(object):
    """
    Encapsulates the details of the Function that don't have todo with a
        specific frame. These details include:
        * function_name
        * file_path
        * line_number
        * docstring
        * code
    """

    def __init__(self, py_frame, **kwargs):
        self.function_name = py_frame.f_code.co_name
        self.file_path = py_frame.f_code.co_filename
        self.line_number = py_frame.f_code.co_firstlineno
        self.func_code = FuncCode(self)
        self.func_docstring = FuncDocstring(self)
    
    """ GETTERS """
    @property
    def code(self):
        """
        Return the code for this function
        """
        return self.func_code.code

    # TODO: ADD FORMATTED DOCSTRING METHOD
    @property
    def docstring(self):
        """
        Return the docstring for this function
        """
        return self.func_docstring.docstring

    # TODO: ADD FILEPATH FUNCTION
    @property
    def file_name(self):
        """
        Returns the file_name that this function resides in
        """
        file_name = self.file_path.split('/')[-1]
        return file_name

    @property
    def file_path(self):
        """
        Returns the file_path that this function resides in
        """
        return self._file_path

    # TODO: CHANGE function_name TO name
    #   * it's just redundant if I keep function_name
    @property
    def function_name(self):
        """
        Return the name of the function
        """
        return self._function_name

    @property
    def func_code(self):
        """
        Return the func_code object associated with this function
        """
        return self._func_code

    @property
    def func_docstring(self):
        """
        Return the func_docstring object associated with this function
        """
        return self._func_docstring

    @property
    def line_number(self):
        """
        Return the line number of where the function is in a file
        """
        return self._line_number

    """ SETTERS """
    @docstring.setter
    def docstring(self, value):
        """
        Sets the value for the docstring object for this function
        """
        self._docstring = value

    @file_path.setter
    def file_path(self, value):
        """
        Sets the value for the file_path for this function
        """
        self._file_path = value

    @function_name.setter
    def function_name(self, value):
        """
        Sets the value for the function_name for this function
        """
        self._function_name = value

    @func_code.setter
    def func_code(self, value):
        """
        Sets the value for the func_code object
        """
        self._func_code = value

    @func_docstring.setter
    def func_docstring(self, value):
        """
        Sets the value for the func_docstring object
        """
        self._func_docstring = value

    @line_number.setter
    def line_number(self, value):
        """
        Sets the value for the line number that this function is at
        """
        self._line_number = value
