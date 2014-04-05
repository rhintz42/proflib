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

    
    def test_frame_called_by_function_name(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.called_by_function_name == 'test_function_name'

    
    def test_frame_called_by_function_name_robust(self):
        from proflib.models.frame import Frame

        parent_frame = Frame(FrameMock(function_name='parent'))
        frame = Frame(FrameMock(f_back=parent_frame.frame))

        assert frame.called_by_function_name == 'parent'

    def test_frame_get_frame(self):
        from proflib.models.frame import Frame

        py_frame = FrameMock()

        frame = Frame(py_frame)

        assert frame.frame.f_locals['a'] == py_frame.f_locals['a']

    def test_frame_back_wrapper(self):
        from proflib.models.frame import Frame

        grandparent_frame = Frame(FrameMock(function_name='grandparent'))
        wrapper_frame = Frame(FrameMock(function_name='wrapped', f_back=grandparent_frame.frame))
        
        frame = Frame(FrameMock(f_back=wrapper_frame.frame))
        
        assert frame.called_by_function_name == 'grandparent'

    def test_frame_back_wrapper(self):
        from proflib.models.frame import Frame

        grandparent_frame = Frame(FrameMock(function_name='grandparent'))
        wrapper_frame = Frame(FrameMock(function_name='wrapped', f_back=grandparent_frame.frame))
        
        frame = Frame(FrameMock(f_back=wrapper_frame.frame))
        
        assert frame.called_by_function_name == 'grandparent'
    
    def test_time(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.time > 0

    def test_pos_default(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.pos_called_in == 0

    def test_pos_passed_in(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock(), pos=4)

        assert frame.pos_called_in == 4

    def test_parent_default(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        assert frame.parent == None

    def test_parent_passed_in(self):
        from proflib.models.frame import Frame

        parent_frame = Frame(FrameMock())

        frame = Frame(FrameMock(), parent=parent_frame)

        assert frame.parent == parent_frame

    def test_to_dict_simple(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        response = frame.to_dict();

        assert 'a' in response['local_variables']

    def test_to_dict_include_variables__simple(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        response = frame.to_dict(include_variables=['a']);

        assert 'a' in response['local_variables']

    def test_to_dict_include_variables__simple_2(self):
        from proflib.models.frame import Frame

        frame = Frame(FrameMock())

        response = frame.to_dict(include_variables=['b']);

        assert 'a' not in response['local_variables']
