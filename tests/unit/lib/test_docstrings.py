try:
    import unittest2 as unittest
except:
    import unittest
import sys


class TestDocStrings(unittest.TestCase):
    
    def test_load_from_file(self):
        from proflib.lib.filelib import get_mod_from_file

        cls = get_mod_from_file('/opt/webapp/proflib/src/proflib/proflib/views.py')

        assert cls

    def test_get_function_code__bar(self):
        from proflib.lib.filelib import get_function_code

        code = get_function_code('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                 'bar')

        assert code[0] == '#@test()\n'

    def test_get_function_code__foo(self):
        from proflib.lib.filelib import get_function_code

        code = get_function_code('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                 'foo')

        assert '@prof(3)' in code[0]

    def test_get_function_code__my_view(self):
        from proflib.lib.filelib import get_function_code

        code = get_function_code('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                 'my_view')

        assert '@view_config' in code[0]

    def test_get_function_code__fo(self):
        from proflib.lib.filelib import get_function_code

        code = get_function_code('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                 'fo')

        assert 'def fo' in code[0]

    def test_get_function_code__add_headers(self):
        from proflib.lib.filelib import get_function_code

        code = get_function_code('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                 'add_headers')

        assert len(code)
        assert code[0] == 'def add_headers(self, request, **kwargs):\n'

    def test_get_function_docstring__foo(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'foo')

        assert docstring[0] == '    """ foo here (A bit bigger than the others) """\n'

    def test_get_function_docstring__fo(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'fo')

        assert docstring[0] == '    """ fo here """\n'

    def test_get_function_docstring__ba(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'ba')

        assert docstring == []

    def test_get_function_docstring__longer_docstring(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'longer_docstring')

        assert len(docstring) == 5
        assert docstring[3] == "    '''Pretty cool'''\n"

    
    def test_get_function_docstring__add_headers(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'add_headers')

        assert len(docstring) == 11
        assert docstring[0] == '    """Add any headers needed by the connection. As of v2.0 this does\n'
    

    def test_get_function_docstring__my_view(self):
        from proflib.lib.filelib import get_function_docstring

        docstring = get_function_docstring('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                           'my_view')

        assert docstring == []

    def test_find_line_number_of_function_definition__foo(self):
        from proflib.lib.filelib import _find_function_definition_line_number, \
                                        get_file_lines

        file_lines = get_file_lines('/opt/webapp/proflib/src/proflib/proflib/views.py')

        line_number = _find_function_definition_line_number(file_lines,
                                                            'foo')

        assert line_number == 52

    def test_find_function_line_number__foo(self):
        from proflib.lib.filelib import _find_function_line_number, \
                                        get_file_lines

        file_lines = get_file_lines('/opt/webapp/proflib/src/proflib/proflib/views.py')

        line_number = _find_function_line_number(file_lines,
                                                 function_def_line_num=52)

        assert line_number == 51

    def test_find_function_line_number__foo_with_function_name(self):
        from proflib.lib.filelib import find_function_line_number

        file_path = '/opt/webapp/proflib/src/proflib/proflib/views.py'
        function_name = 'foo'

        line_number = find_function_line_number(file_path,
                                                function_name=function_name)

        assert line_number == 51

    def test_find_function_line_number__foo_with_function_def_line_num(self):
        from proflib.lib.filelib import find_function_line_number

        file_path = '/opt/webapp/proflib/src/proflib/proflib/views.py'
        function_def_line_num = 52

        line_number = find_function_line_number(file_path,
                                                function_def_line_num=function_def_line_num)

        assert line_number == 51
