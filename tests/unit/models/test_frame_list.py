try:
    import unittest2 as unittest
except:
    import unittest

import sys


class FrameCodeMock(object):
    def __init__(self, *args, **kwargs):
        self.co_name = kwargs['function_name'] if 'function_name' in kwargs else 'test_function_name'
        self.co_filename = 'test_filename'
        

class FrameMock(object):
    def __init__(self, *args, **kwargs):
        self.frame = self
        self.f_code = FrameCodeMock(**kwargs)
        self.f_locals = {'a': 'b'}
        self.f_back = kwargs['f_back'] if 'f_back' in kwargs else self

class TestFrameList(unittest.TestCase):

    def test_frame_list_init_simple_functions_list(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._ordered_functions_list) == 0

    def test_frame_list_init_simple_frame_map(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._frame_map) == 0
