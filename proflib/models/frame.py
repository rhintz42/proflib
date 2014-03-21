import sys
import os
import time

class Frame(object):
    """
    Encapsulates a function and contains all the local variables and such,
        formatted in the correct way for easy copy and paste into tests
    """
    # AD IDs to this so that Can Remain Unique
    def __init__(self, *args, **kwargs):
        self._init_with_frame(args[0], **kwargs)

    def _init_with_frame(self, frame, **kwargs):
        self.parent = kwargs['parent'] if 'parent' in kwargs else None
        self.children = kwargs['children'] if 'children' in kwargs else []
        self.frame = frame
        self.function_name = frame.f_code.co_name
        self.filename = frame.f_code.co_filename
        self.local_variables = frame.f_locals.copy()
        self.time = time.time()
        self.called_by_function_name = frame.f_back.f_code.co_name
        self.pos_called_in = kwargs['pos'] if 'pos' in kwargs else 0

    """ GETTERS """
    @property
    def called_by_function_name(self):
        return self._called_by_function_name

    @property
    def children(self):
        return self._children

    @property
    def filename(self):
        return self._filename

    @property
    def frame(self):
        return self._frame

    @property
    def function_name(self):
        return self._function_name

    @property
    def local_variables(self):
        return self._local_variables

    @property
    def parent(self):
        return self._parent

    @property
    def pos_called_in(self):
        return self._pos_called_in

    @property
    def time(self):
        return self._time

    """ SETTERS """
    @called_by_function_name.setter
    def called_by_function_name(self, value):
        self._called_by_function_name = value

    @children.setter
    def children(self, value):
        self._children = value

    @filename.setter
    def filename(self, value):
        self._filename = value

    @frame.setter
    def frame(self, value):
        self._frame = value

    @function_name.setter
    def function_name(self, value):
        self._function_name = value

    @local_variables.setter
    def local_variables(self, value):
        self._local_variables = value

    @parent.setter
    def parent(self, value):
        self._parent = value

    @pos_called_in.setter
    def pos_called_in(self, value):
        self._pos_called_in = value

    @time.setter
    def time(self, value):
        self._time = value

    def prepend_child(self, frame):
        self.children.insert(0, frame)
    
    def to_dict(self):
        return {
            'called_by_function_name': self.called_by_function_name,
            'children': [c.to_dict() for c in self.children],
            'filename': self.filename,
            'function_name': self.function_name,
            'local_variables': self.local_variables,
            'parent': self.parent,
            'pos_called_in': self.pos_called_in,
            'time': self.time,
        }
