from pyramid.view import view_config
from proflib.lib.decorators import prof
from proflib.models.frame_list import FrameList
from proflib.models.frame import Frame
#from .views2 import hello
from proflib.views2 import hello


def fo():
    """ fo here """
    c = 30
    return c


@prof(1)
def ba(var):
    d = var
    return d


@prof()
def tt():
    z = 20
    f = fo()
    return z


#@test()
#@prof()
def bar(tr):
    b = 20
    if tr:
        d = ba(3)
        k = ba('j')
    else:
        d = ba(4)
        k = ba('z')
        
    return b


@view_config(route_name='home', renderer='json')
def my_view(request):
    print("!Nice!")
    a = foo()
    b = bar(True)
    b = bar(False)
    return {'project': 'proflib'}


@prof(3)
def foo():
    """ foo here (A bit bigger than the others) """
    a = 10
    e = bar(True)
    c = fo()
    g = bar(False)
    h = tt()
    x = longer_docstring()
    return a

#@otherprof
@prof(2)
def longer_docstring():
    """
    This is the docstring for the function longer_docstring
    It is called by foo
    '''Pretty cool'''
    """
    x = 84
    return x
