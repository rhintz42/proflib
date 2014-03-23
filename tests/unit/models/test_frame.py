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
        self.f_back = self


class TestFrame(unittest.TestCase):
    
    def test_frame_init_simple(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame

    
    def test_frame_filename(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.filename == 'test_filename'

    
    def test_frame_local_variables(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.local_variables['a'] == 'b'

    
    """
    def test_frame_actual_frame(self):
        from proflib.models.frame import Frame

        frame = sys._getframe(0)
        frame = Frame(FrameMock())

        assert frame.local_variables['a'] == 'b'
    """
