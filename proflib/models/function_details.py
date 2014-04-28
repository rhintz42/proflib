from parsefilelib.models.base_lines_obj import BaseLinesObj

class FunctionDetails(BaseLinesObj):
    """
    Encapsulates the details of the Function that don't have todo with a
        specific frame. These details include:
        * file specific implementation of name
    """

    def __init__(self, py_frame, **kwargs):
        line_number = py_frame.f_code.co_firstlineno
        name = py_frame.f_code.co_name
        file_path = py_frame.f_code.co_filename

        super(FunctionDetails, self).__init__(def_name=name,
                                              file_path=file_path,
                                              line_number=line_number)

        # If this frame object is not associated with a file, then just set
        #   some basic things for the frame so can get by
        #   TODO: Eventually refactor this into parsefilelib
        if not self.has_file:
            self.name = py_frame.f_code.co_name
    
    """ GETTERS """
    @property
    def has_file(self):
        if self.parent_file:
            return True
        return False

    @property
    def name(self):
        """
        Return the name of the function
        """
        if self.has_file:
            return super(FunctionDetails, self).name
        return self._name

    """ SETTERS """
    @name.setter
    def name(self, value):
        """
        Sets the value for the name for this function

        NOTE: This should only be used in the situation where the function is
            not associated with the file passed in, like in tests. If this
            function is associated with a file, then this property won't be
            used
        """
        self._name = value
