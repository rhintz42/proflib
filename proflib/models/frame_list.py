import sys
import os
import time
from proflib.models.frame import Frame

class FrameList(object):
    """
    Encapsulates a function and contains all the local variables and such,
        formatted in the correct way for easy copy and paste into tests
    """
    def __init__(self, *args, **kwargs):
        # Ordered by when function finished
        self._ordered_functions_list = []
        self._frame_map = {}

    def add_frame(self, frame):
        function_name = frame.f_code.co_name
        key = function_name + str(self.num_frames)
        self.add_to_ordered_functions_list(key)
        self._frame_map[key] = Frame(frame, pos=self.num_frames)
        
    def add_to_ordered_functions_list(self, value):
        self._ordered_functions_list.append(value)

    @property
    def find_frame(self, function_name):
        pass

    @property
    def frame_map(self):
        return self._frame_map
    
    @property
    def ordered_functions_list(self):
        return self._ordered_functions_list
    
    @property
    def num_frames(self):
        return len(self.ordered_functions_list)

    @property
    def reverse_order_functions_list(self):
        return self.ordered_functions_list[::-1]

    def rec_build_hierarchy(self, reversed_order_list, root_frame, pos):
        #import pdb;pdb.set_trace()
        while pos < self.num_frames:
            current_frame = self.frame_map[reversed_order_list[pos]]
            if current_frame.called_by_function_name != root_frame.function_name:
                return pos-1

            root_frame.prepend_child(current_frame)

            pos = self.rec_build_hierarchy(reversed_order_list, current_frame, pos+1)

            pos = pos + 1

        return pos

    def build_hierarchy(self):
        function_map = {}

        reversed_order_list = self.reverse_order_functions_list
        root_key = reversed_order_list[0]
        root_frame = self.frame_map[root_key]
        pos = 0
        while pos < self.num_frames:
            pos = self.rec_build_hierarchy(reversed_order_list, root_frame, pos+1) + 1
            if pos < self.num_frames:
                root_frame = self.frame_map[reversed_order_list[pos]]
        
        return root_frame
