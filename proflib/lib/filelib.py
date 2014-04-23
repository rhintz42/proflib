import imp
import os
import inspect

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
        print('filepath: ' + filepath)
        print(e)
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
        #print('IOError - File does not exist')
        #print('Filepath: ' + filepath)
        #print(e)
        return []
    
    return file_lines

def get_function_definition(function_name):
    """
    Return start of string representation of function with the given function
        name
    """
    return 'def %s' %(function_name)

def find_function_line_number(filepath, function_name=None,
                              function_def_line_num=None):
    """
    Return line number of start of the function

    Return -1 if function not in file

    This includes the decorators of the function
    """
    file_lines = get_file_lines(filepath)

    if not function_def_line_num and function_name:
        function_def_line_num = _find_function_definition_line_number(file_lines,
                                                                      function_name)
    
    return _find_function_line_number(file_lines,
                                      function_def_line_num=function_def_line_num)


def _find_function_definition_line_number(file_lines, function_name):
    """
    Return the line number where the function is defined in the file

    Return -1 if the function_name not found in the file
    """
    function_definition = get_function_definition(function_name)

    for i,l in enumerate(file_lines):
        if function_definition in l:
            return i + 1

    return -1

def _find_function_line_number(file_lines,
                               function_def_line_num):
    """
    Return the line number of the highest decorator of the function

    Return the line_number of the function definition if no decorators on
        function
    """
    i = function_def_line_num - 1
    while(i >= 0):
        if '@' not in file_lines[i] and 'def' not in file_lines[i]:
            return i + 2 # +1 to accomodate the 0 index of file_lines and +1
                         #  because the previous line had the last
                         #  decorator/function definition
        i -= 1

    if i == 0:
        return 0

    return function_def_line_num

def is_trace_wrapper_function(source_lines):
    if source_lines[0][0] == '        @wraps(func)    # TRACE WRAPPER\n':
        return True
    return False

def get_func_from_mod(mod, function_name):
    if hasattr(py_mod, function_name):
        return getattr(py_mod, function_name)

def _find_function_end_line_number(file_lines, function_def_line_num):
    # Get indent
    function_def_indent = len(file_lines[function_def_line_num-1]) - len(file_lines[function_def_line_num-1].lstrip())

    for i in xrange(function_def_line_num + 1, len(file_lines)):
        current_line_indent = len(file_lines[i]) - len(file_lines[i].lstrip())
        if '\n' != file_lines[i] and current_line_indent <= function_def_indent:
            return i
    return len(file_lines)

def _get_function_lines(lines, function_line_num, function_end_line_num):
    return lines[function_line_num-1:function_end_line_num]

def get_function_code(filepath, function_name):
    file_lines = get_file_lines(filepath)

    function_def_line_num = _find_function_definition_line_number(file_lines,
                                                                  function_name)
    
    if function_def_line_num < 0:
        # print('FUNCTION NOT FOUND: ' + function_name)
        # print('FILEPATH: ' + filepath)
        return []

    function_line_num = _find_function_line_number(file_lines,
                                                   function_def_line_num)

    function_end_line_num = _find_function_end_line_number(file_lines,
                                                           function_def_line_num)

    func_code_lines = _get_function_lines(file_lines, function_line_num, function_end_line_num)

    return func_code_lines

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

def get_function_docstring(filepath, function_name):
    """
    Return the docstring lines of the function
    """
    func_code_lines = get_function_code(filepath, function_name)
    
    if not _has_docstring(func_code_lines, function_name):
        return []

    docstring_start_index = _get_docstring_start_index(func_code_lines, function_name)

    # get ending_docstring_index
    docstring_end_index = _get_docstring_end_index(func_code_lines,
                                                   docstring_start_index)

    if docstring_end_index < 0:
        print("ERROR IN get_function_docstring!!!")
        print(func_code_lines)
        print(docstring_start_index)
        print("!!!")
        return []

    return func_code_lines[docstring_start_index:docstring_end_index+1]
