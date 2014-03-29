import sys
import os
import time
from proflib.models.frame import Frame


def get_function_key(function_name, num_frames):
    """
    Returns the function_key
    """
    return function_name + str(num_frames)

class FrameList(object):
    """
    Encapsulates a function and contains all the local variables and such,
        formatted in the correct way for easy copy and paste into tests
    """

    def __init__(self, *args, **kwargs):
        """
        The init function for the FrameList class
        """
        self._ordered_functions_list = []
        self._frame_map = {}
        self._root_frames = []

    def add_frame(self, frame):
        """
        Adds a frame to this class, adding it to the:
            * ordered_functions_list 
            * frame_map
        When adding to the frame_map, creates a new Frame object, encapsulating
            the Python Frame Object
        """
        function_name = frame.f_code.co_name
        key = get_function_key(function_name, self.num_frames)
        self.add_to_ordered_functions_list(key)
        self._frame_map[key] = Frame(frame, pos=self.num_frames)
        
    def add_to_ordered_functions_list(self, function_key):
        """
        Adds the function_key to the ordered_functions_list
        """
        self._ordered_functions_list.append(function_key)

    def find_frames(self, function_name):
        """
        Finds all the function frames that have the specified function_name
        """
        pass

    @property
    def frame_map(self):
        """
        Returns the frame_map

        The _frame_map consists of:
        * Keys: The keys are the frame's function_name & position finished in
        * Values: The Frame object associated with the function_name
        """
        return self._frame_map
    
    @property
    def ordered_functions_list(self):
        """
        Returns the _ordered_functions_list

        The _ordered_functions_list is list of all the function_key's, ordered
            by when the function finished execution (i.e. returned)
        """
        return self._ordered_functions_list
    
    @property
    def num_frames(self):
        """
        Returns the length of the _ordered_functions_list, which is the number
            of Frames Created
        """
        return len(self.ordered_functions_list)

    @property
    def root_frames(self):
        """
        Returns all of the root_frames, or all the frames that had the wrapped
            function on them that don't have an ancestor that had the wrapped
            function applied to them
        """
        return self._root_frames

    @property
    def reverse_order_functions_list(self):
        """
        Return a list that is in reversed order of the ordered_functions_list
        """
        return self.ordered_functions_list[::-1]

    def _rec_build_hierarchy(self, reversed_order_list, root_frame, pos):
        """
        The recursive wrapper for build_hierarchy
        """
        while pos < self.num_frames:
            current_frame = self.frame_map[reversed_order_list[pos]]
            if current_frame.called_by_function_name != root_frame.function_name:
                return pos-1

            root_frame.prepend_child(current_frame)

            pos = self._rec_build_hierarchy(reversed_order_list, current_frame, pos+1)

            pos = pos + 1

        return pos

    def build_hierarchy(self):
        """
        Build a hierarchy of Frames to Frames

        Returns the root_frame
        """
        function_map = {}

        reversed_order_list = self.reverse_order_functions_list
        if len(reversed_order_list) == 0:
            return
        root_key = reversed_order_list[0]
        root_frame = self.frame_map[root_key]
        self._root_frames.append(root_frame)
        pos = 0
        while pos < self.num_frames:
            pos = self._rec_build_hierarchy(reversed_order_list, root_frame, pos+1) + 1
            if pos < self.num_frames:
                root_frame = self.frame_map[reversed_order_list[pos]]
                self._root_frames.append(root_frame)

        
        return root_frame

    # TODO: THE CHILDREN LIST SHOULD BE AN OBJECT (MAYBE FRAME_LIST?)
    def to_json_output(self, depth=2):
        """
        Return a list of Frames that have been converted to dicts for easy
            output
        """
        if depth <= 0:
            return []

        output_list = []
        for frame in self.root_frames:
            output_list.append(frame.to_dict(depth=depth))

        return output_list
