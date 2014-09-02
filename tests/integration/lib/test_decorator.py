try:
    import unittest2 as unittest
except:
    import unittest
import sys

from proflib.lib.decorators import prof


class Foo(object):
    @classmethod
    @prof()
    def bar(cls, a, b):
        return {
            'a': a,
            'b': b,
        }


class TestProf(unittest.TestCase):

    def test_trace(self):
        pass

    def test_class_method(self):
        result = Foo.bar(10, 20)
        assert result == {
            'a': 10,
            'b': 20,
        }
