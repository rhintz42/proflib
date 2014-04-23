from proflib.lib.parsefilelib import get_file_lines

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
        # TODO: ERROR LOGGING
        return []

    function_line_num = _find_function_line_number(file_lines,
                                                   function_def_line_num)

    function_end_line_num = _find_function_end_line_number(file_lines,
                                                           function_def_line_num)

    func_code_lines = _get_function_lines(file_lines, function_line_num, function_end_line_num)

    return func_code_lines

