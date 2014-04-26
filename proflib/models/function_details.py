import sys
import os
import time
import traceback
from parsefilelib.models.file_obj import FileObj
from parsefilelib.models.base_lines_obj import BaseLinesObj

class FunctionDetails(BaseLinesObj):
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
        self.line_number = py_frame.f_code.co_firstlineno
        #self.file_obj = self.fetch_file_obj(py_frame.f_code.co_filename)

        line_number = py_frame.f_code.co_firstlineno
        function_name = py_frame.f_code.co_name
        file_path = py_frame.f_code.co_filename

        super(FunctionDetails, self).__init__(def_name=function_name,
                                                file_path=file_path)
        if self.has_file:
            # TODO: PASS IN LINE NUMBER TO THIS FUNCTION SO CAN BE SURE HAVE
            #   CORRECT FUNCTION, OTHERWISE CAN"T TELL BETWEEN DIFFERENT CLASSES
            self.function_obj = self.fetch_function_obj(py_frame.f_code.co_name)

        if not self.has_function:
            self.function_name = py_frame.f_code.co_name
            self.file_path = py_frame.f_code.co_filename
    
    """ GETTERS """
    @property
    def has_file(self):
        if self.file_obj:
            return True
        return False

    @property
    def has_function(self):
        if self.function_obj:
            return True
        return False

    @property
    def code(self):
        """
        Return the code for this function

        Alias for lines
        """
        return self.lines

    #@property
    #def lines(self):
    #    """
    #    Return the code for this function
    #    """
    #    if self.has_function:
    #        return self.function_obj.lines
    #    return []

    #@property
    #def decorators(self):
    #    """
    #    Return the code for this function
    #    """
    #    if self.has_function:
    #        return self.function_obj.decorators
    #    return []

    # TODO: ADD FORMATTED DOCSTRING METHOD
    #@property
    #def docstring(self):
    #    """
    #    Return the docstring for this function
    #    """
    #    if self.has_function:
    #        return self.function_obj.docstring
    #    return self._docstring

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
        return self.file_obj.path

    @property
    def file_obj(self):
        """
        Returns the file object
        """
        return self.parent_file

    # TODO: CHANGE function_name TO name
    #   * it's just redundant if I keep function_name
    @property
    def function_name(self):
        """
        Return the name of the function
        """
        if self.has_function:
            return self.function_obj.name
        return self._function_name

    @property
    def function_obj(self):
        """
        Return the function object gotten from the file_obj
        """
        if hasattr(self, '_function_obj'):
            return self._function_obj
        return None

    @property
    def line_number(self):
        """
        Return the line number of where the function is in a file
        """
        return self._line_number

    """ SETTERS """
    #@docstring.setter
    #def docstring(self, value):
    #    """
    #    Sets the value for the docstring object for this function
    #    """
    #    if self.has_function:
    #        self._function_obj.append_docstring(value)
    #    else:
    #        self._docstring = value

    @file_path.setter
    def file_path(self, value):
        """
        Sets the value for the file_path for this function
        """
        self._file_path = value

    #@file_obj.setter
    #def file_obj(self, value):
    #    """
    #    Sets the value for the file_obj for this function
    #    """
    #    self._file_obj = value

    @function_obj.setter
    def function_obj(self, value):
        """
        Sets the value for the function_obj for this function
        """
        self._function_obj = value

    
    @function_name.setter
    def function_name(self, value):
        """
        Sets the value for the function_name for this function
        """
        if self.has_function:
            self._function_obj.name = value
        else:
            self._function_name = value

    @line_number.setter
    def line_number(self, value):
        """
        Sets the value for the line number that this function is at
        """
        self._line_number = value


    """ FETCH FUNCTIONS """
    #def fetch_file_obj(self, path):
    #    return FileObj(path)


    def fetch_function_obj(self, function_name):
        return self.rec_fetch_function_obj(self.file_obj, function_name)
        

    def rec_fetch_function_obj(self, obj, function_name):
        for f in obj.functions:
            if f.name == function_name:
                return f

        for f in obj.functions:
            self.rec_fetch_function_obj(f, function_name)

        for c in obj.functions:
            self.rec_fetch_function_obj(c, function_name)

        return None
