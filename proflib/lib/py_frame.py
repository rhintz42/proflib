def get_py_frame_locals(py_frame):
    return py_frame.f_locals.copy()

def get_py_frame_called_by_function(py_frame, wrapper_function_name):
    if py_frame.f_back.f_code.co_name == wrapper_function_name:
        return py_frame.f_back.f_back.f_code.co_name

    return py_frame.f_back.f_code.co_name
