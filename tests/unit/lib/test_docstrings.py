try:
    import unittest2 as unittest
except:
    import unittest
import sys


class TestDocStrings(unittest.TestCase):
    
    def test_load_from_file(self):
        from proflib.lib.docstrings import get_mod_from_file

        cls = get_mod_from_file('/opt/webapp/proflib/src/proflib/proflib/views.py')

        assert cls

    def test_get_code_of_function__bar(self):
        from proflib.lib.docstrings import get_code_of_function

        code = get_code_of_function('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                    'bar',
                                    39)

        assert code

    def test_get_code_of_function__foo(self):
        from proflib.lib.docstrings import get_code_of_function

        code = get_code_of_function('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                    'foo',
                                    49)

        assert code

    def test_get_code_of_function__my_view(self):
        from proflib.lib.docstrings import get_code_of_function

        code = get_code_of_function('/opt/webapp/proflib/src/proflib/proflib/views.py',
                                    'my_view',
                                    51)

        assert code
