import sys
import os
import time

class Frame(object):
    """
    Encapsulates the Python Frame Object and contains all the local variables
        and such. When asked to print, formats the data in a way for easy copy
        and paste into tests
    """
    # TODO: ADD SETTING THE PARENT WHEN ADDING CHILD

    # TODO: BE ABLE TO ADD FORMATTING FOR DISPLAYING
    #   * Maybe add something between children functions
    #   * Should probably be in the format library

    # TODO: Change the kwargs to variables of the map that I actually want to
    #   allow
    def __init__(self, frame, **kwargs):
        """
        Init method for the Frame class
        """
        self._init_with_frame(frame, **kwargs)

    # TODO: Add setters for each variable
    # TODO: Change the **kwargs to have the specific key-word arguments that
    #   this method takes
    def _init_with_frame(self, frame, **kwargs):
        """
        Initializes the frame object with the Python Frame Object provided.
        """
        self.wrapper_function_name = 'wrapped'

        self.parent = kwargs['parent'] if 'parent' in kwargs else None
        self.children = kwargs['children'] if 'children' in kwargs else []
        self.frame = frame
        self.function_name = frame.f_code.co_name
        self.filename = frame.f_code.co_filename
        self.local_variables = frame.f_locals.copy()
        self.time = time.time()
        if frame.f_back.f_code.co_name == self.wrapper_function_name:
            self.called_by_function_name = frame.f_back.f_back.f_code.co_name
        else:
            self.called_by_function_name = frame.f_back.f_code.co_name
        self.pos_called_in = kwargs['pos'] if 'pos' in kwargs else 0

    """ GETTERS """
    @property
    def called_by_function_name(self):
        """
        Returns the name of the function that this frame/function was called by
        """
        return self._called_by_function_name

    @property
    def children(self):
        """
        Returns all of the frames/functions that this frame/function called
        """
        return self._children

    @property
    def filename(self):
        """
        Returns the filename that this function resides in
        """
        return self._filename

    @property
    def frame(self):
        """
        Returns the Python Frame Object associated with this Frame
        """
        return self._frame

    @property
    def function_name(self):
        """
        Returns the function name of this frame/function
        """
        return self._function_name

    @property
    def local_variables(self):
        """
        Returns the local variables of this frame/function
        """
        return self._local_variables

    @property
    def parent(self):
        """
        Returns the frame that called this frame/function
        """
        return self._parent

    @property
    def pos_called_in(self):
        """
        Returns the "position" that this frame/function finished in relation
            to the other functions that the function that had the wrapper
            applied to it was called.
        The first function to finish will have a position closest to 0
        """
        return self._pos_called_in

    @property
    def time(self):
        """
        Returns the time that this frame/function returned
        """
        return self._time

    """ SETTERS """
    @called_by_function_name.setter
    def called_by_function_name(self, value):
        """
        Sets the value for self.called_by_function_name
        """
        self._called_by_function_name = value

    @children.setter
    def children(self, value):
        """
        Sets the value for self.children
        """
        self._children = value

    @filename.setter
    def filename(self, value):
        """
        Sets the value for self.filename
        """
        self._filename = value

    @frame.setter
    def frame(self, value):
        """
        Sets the value for self.frame
        """
        self._frame = value

    @function_name.setter
    def function_name(self, value):
        """
        Sets the value for self.function_name
        """
        self._function_name = value

    @local_variables.setter
    def local_variables(self, value):
        """
        Sets the value for self.local_variables
        """
        self._local_variables = value

    @parent.setter
    def parent(self, value):
        """
        Sets the value for self.parent
        """
        self._parent = value

    @pos_called_in.setter
    def pos_called_in(self, value):
        """
        Sets the value for self.pos_called_in
        """
        self._pos_called_in = value

    @time.setter
    def time(self, value):
        """
        Sets the value for self.time
        """
        self._time = value

    # TODO: WHAT ARE THE FRAME OBJECTS WE ARE INSERTING?
    #   They are this class objects, but we should specify the difference
    #       between this class and regular python frames
    def prepend_child(self, frame):
        """
        Add a frame to the beginning of the children list if the function is
            not the wrapper_function
        """
        if frame.function_name != self.wrapper_function_name:
            self.children.insert(0, frame)

    def _get_local_variables_to_include(self, include_variables):
        if not include_variables:
            return self.local_variables

        local_variables = {}
        for key,value in self.local_variables.items():
            if key in include_variables:
                local_variables[key] = value

        return local_variables
    
    def to_dict(self, depth=2, include_keys=None, include_variables=None,
                exclude_keys=None, exclude_variables=None):
        """
        Recursively print out all of the frames and their children, and return
            in a dict format for easier printing to console/file
        The depth signifies how deep into the children you want to go in the
            recursion
        """
        if depth <= 0:
            return None
        new_depth = depth - 1

        local_variables = self._get_local_variables_to_include(include_variables)

        return {
            'called_by_function_name': self.called_by_function_name,
            'children': [c.to_dict( depth=new_depth, include_keys=include_keys, \
                                    include_variables=include_variables, \
                                    exclude_keys=exclude_keys, \
                                    exclude_variables=exclude_variables) for c in self.children],
            'filename': self.filename,
            'function_name': self.function_name,
            'local_variables': local_variables,
            'parent': self.parent,
            'pos_called_in': self.pos_called_in,
            'time': self.time,
        }
