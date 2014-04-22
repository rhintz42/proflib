# This code taken from:
#   http://stackoverflow.com/questions/301134/dynamic-module-import-in-python
import imp
import os
import inspect

def get_mod_from_file(filepath):
    class_inst = None
    expected_class = 'MyClass'

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        return imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        return imp.load_compiled(mod_name, filepath)

    return None

def get_docstring_of_function(filepath, function_name):
    py_mod = get_mod_from_file(filepath)

    if hasattr(py_mod, function_name):
        func = getattr(py_mod, function_name)
        docstring = func.__doc__
        if docstring:
            return docstring 
    
    return ""

def is_trace_wrapper_function(source_lines):
    if source_lines[0][0] == '        @wraps(func)    # TRACE WRAPPER\n':
        return True
    return False

def get_code_of_function(filepath, function_name, line_number):
    py_mod = get_mod_from_file(filepath)

    if hasattr(py_mod, function_name):
        func = getattr(py_mod, function_name)
        filename = inspect.getfile(func)
        mod = inspect.getmodule(func)
        lines = inspect.getsourcelines(func)
        first_line_code = lines[0][0]
        if not is_trace_wrapper_function(lines):
            return lines

    return _get_code_of_trace_wrapped_function(filepath, function_name, line_number)

def _get_code_of_trace_wrapped_function(filepath, function_name, line_number):
    py_mod = get_mod_from_file(filepath)

    if hasattr(py_mod, function_name):
        func = getattr(py_mod, function_name)
    
    with open(filepath) as f:
        file_lines = f.readlines()

    index_start_func = line_number - 1;

    # Have the line line number to start with 1 after the wrappers
    for i in xrange(index_start_func, len(file_lines)):
        if "def" in file_lines[i]:
            function_def_start = i
            break

    for i in xrange(function_def_start + 1, len(file_lines)):
        if "def" in file_lines[i] or "@" in file_lines[i]:
            index_end_func = i
            break

    if 'index_end_func' not in locals():
        index_end_func = len(file_lines)

    func_list = file_lines[index_start_func:index_end_func]

    return func_list

