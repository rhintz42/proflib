try:
    import unittest2 as unittest
except:
    import unittest

import sys


class FrameCodeMock(object):
    def __init__(self, *args, **kwargs):
        self.co_name = kwargs['function_name'] if 'function_name' in kwargs else 'test_function_name'
        self.co_filename = 'test_filename'
        

class PyFrameMock(object):
    def __init__(self, *args, **kwargs):
        self.frame = self
        self.f_code = FrameCodeMock(**kwargs)
        self.f_locals = {'a': 'b'}
        self.f_back = kwargs['f_back'] if 'f_back' in kwargs else self

class TestFrameList(unittest.TestCase):

    def test_get_function_key(self):
        from proflib.models.frame_list import get_function_key

        key = get_function_key('test_function_name', 32)

        assert key == 'test_function_name32'

    def test_init_simple_functions_list(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._ordered_functions_list) == 0

    def test_init_simple_frame_map(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._frame_map) == 0

    def test_init_simple_root_frames(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._frame_map) == 0

    def test_init_simple_root_frames(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list._frame_map) == 0

    def test_add_frame_simple_added_to_ordered_list(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        frame_list.add_frame(PyFrameMock())
        
        assert len(frame_list.ordered_functions_list) == 1
        assert frame_list.ordered_functions_list[0] == 'test_function_name0'

    def test_add_frame_simple_added_to_frame_map(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        frame_list.add_frame(PyFrameMock())
        
        assert len(frame_list.frame_map) == 1
        assert frame_list.frame_map['test_function_name0']

    def test_append_to_ordered_functions_list(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        frame_list._append_to_ordered_functions_list('test_function_name42')
        
        assert len(frame_list.ordered_functions_list) == 1
        assert frame_list.ordered_functions_list[0] == 'test_function_name42'

    def test_append_to_ordered_functions_list(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        frame_list._append_to_ordered_functions_list('test_function_name42')
        
        assert len(frame_list.ordered_functions_list) == 1
        assert frame_list.ordered_functions_list[0] == 'test_function_name42'

    #----------------------------- find_frames ---------------------------------
    def test_find_frames(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        frame_list.find_frames('test_function_name')
        # TODO: Add tests for this

    #----------------------------- frame_map ---------------------------------
    def test_frame_map_simple(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        assert frame_list.frame_map == {}

    def test_frame_map_one_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        py_frame = PyFrameMock()
        
        frame_list.add_frame(py_frame)
        
        assert len(frame_list.frame_map) == 1


    #------------------------- ordered_functions_list -------------------------
    def test_ordered_functions_list_simple(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        assert len(frame_list.ordered_functions_list) == 0

    def test_ordered_functions_list_one_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        py_frame = PyFrameMock()
        
        frame_list.add_frame(py_frame)
        
        assert len(frame_list.ordered_functions_list) == 1

    #------------------------------ num_frames -------------------------------
    def test_num_frames_simple(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        assert frame_list.num_frames == 0

    def test_num_frames_one_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        py_frame = PyFrameMock()
        
        frame_list.add_frame(py_frame)
        
        assert frame_list.num_frames == 1

    #------------------------------ root_frames -------------------------------
    def test_root_frames_simple(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        assert len(frame_list.root_frames) == 0

    def test_root_frames_one_frame_added(self):
        from proflib.models.frame_list import FrameList
        from proflib.models.frame import Frame

        frame_list = FrameList()

        frame = Frame(PyFrameMock())

        frame_list._append_to_root_frames(frame)
        
        assert len(frame_list.root_frames) == 1

    #------------------------- _append_to_root_frames ------------------------
    def test_append_to_root_frames_one_frame_added(self):
        from proflib.models.frame_list import FrameList
        from proflib.models.frame import Frame

        frame_list = FrameList()

        frame = Frame(PyFrameMock())

        frame_list._append_to_root_frames(frame)
        
        assert len(frame_list.root_frames) == 1

    #---------------------- reverse_order_functions_list ----------------------
    def test_reverse_order_functions_list_simple(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert len(frame_list.reverse_order_functions_list) == 0

    def test_reverse_order_functions_list_one_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        frame_list.add_frame(PyFrameMock())

        assert len(frame_list.reverse_order_functions_list) == 1

    def test_reverse_order_functions_list_one_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()
        
        frame_list.add_frame(PyFrameMock())
        frame_list.add_frame(PyFrameMock(function_name='test2'))

        assert len(frame_list.reverse_order_functions_list) == 2
        assert frame_list.reverse_order_functions_list[0] == 'test21'


    #----------------------------- build_hierarchy ----------------------------
    def test_build_hierarchy_2_frames_added(self):
        from proflib.models.frame_list import FrameList
        from proflib.models.frame import Frame

        py_frame_parent = PyFrameMock(function_name='test_function_name_parent')
        py_frame_child = PyFrameMock(f_back=py_frame_parent, function_name='test_function_name_child')

        frame_list = FrameList()

        frame_list.add_frame(py_frame_child)
        frame_list.add_frame(py_frame_parent)

        frame_list.build_hierarchy()

        root_frame = frame_list.root_frames[0]
        
        assert root_frame.function_name == 'test_function_name_parent'
        assert len(root_frame.children) == 1
        assert root_frame.children[0].function_name == 'test_function_name_child'

    #----------------------------- to_json_output ----------------------------
    def test_to_json_output(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        assert frame_list.to_json_output() == []

    def test_to_json_output_1_frame_added(self):
        from proflib.models.frame_list import FrameList

        frame_list = FrameList()

        frame_list.add_frame(PyFrameMock())

        frame_list.build_hierarchy()

        assert frame_list.to_json_output()[0]['function_name'] == 'test_function_name'

