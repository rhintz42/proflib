def get_py_frame_locals(py_frame):
    """
    Return the locals of a Python Frame object
    """
    return py_frame.f_locals.copy()

def get_py_frame_called_by_function(py_frame, wrapper_function_name):
    """
    Return the function name of this frame's parent frame
    """
    if py_frame.f_back.f_code.co_name == wrapper_function_name:
        return py_frame.f_back.f_back.f_code.co_name

    return py_frame.f_back.f_code.co_name
