import imp
import os

# This code taken from:
#   http://stackoverflow.com/questions/301134/dynamic-module-import-in-python
def get_mod_from_file(filepath):
    class_inst = None

    if 'lib/python2.7' in filepath:
        return None

    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
    
    try:
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)
            return py_mod
        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)
            return py_mod
    except ValueError as e:
        # TODO: ERROR LOGGING
        return None

    return None

def get_file_lines(filepath):
    """
    Return all the lines of a file and return them as an array
    """
    try:
        with open(filepath) as f:
            file_lines = f.readlines()
    except IOError as e:
        # TODO: ERROR LOGGING
        return []
    
    return file_lines


def get_func_from_mod(mod, function_name):
    if hasattr(py_mod, function_name):
        return getattr(py_mod, function_name)
