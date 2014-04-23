from proflib.lib.parsefilelib import get_file_lines
from proflib.lib.func_code import get_function_definition, \
                                  get_function_code

def get_function_docstring(filepath, function_name):
    """
    Return the docstring lines of the function
    """
    func_code_lines = get_function_code(filepath, function_name)
    
    if not _has_docstring(func_code_lines, function_name):
        return []

    docstring_start_index = _get_docstring_start_index(func_code_lines, function_name)

    docstring_end_index = _get_docstring_end_index(func_code_lines,
                                                   docstring_start_index)

    if docstring_end_index < 0:
        # TODO: ERROR LOGGING
        return []

    return func_code_lines[docstring_start_index:docstring_end_index+1]

def _get_docstring_start_index(func_code_lines, function_name):
    """ Get Start of Docstring line # """
    function_definition = get_function_definition(function_name)

    for i,l in enumerate(func_code_lines):
        if(function_definition in l):
            return i + 1
    return -1

def _get_docstring_end_index(func_code_lines, docstring_start_index):
    """ Get End of Docstring line # """
    if func_code_lines[docstring_start_index].count('"""') == 2:
        return docstring_start_index
    
    for i,l in enumerate(func_code_lines[docstring_start_index+1:],
                         start=docstring_start_index+1):
        if '"""' in l:
            return i

    return -1

def _has_docstring(func_code_lines, function_name):
    """ Returns True if func_code_lines has a docstring, false otherwise """
    if len(func_code_lines) == 0:
        return False

    docstring_start_index = _get_docstring_start_index(func_code_lines,
                                                       function_name)

    return docstring_start_index != -1 and '"""' in func_code_lines[docstring_start_index]

